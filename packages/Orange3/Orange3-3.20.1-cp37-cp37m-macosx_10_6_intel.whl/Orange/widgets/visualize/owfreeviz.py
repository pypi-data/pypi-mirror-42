from enum import IntEnum
import sys

import numpy as np

from AnyQt.QtCore import (
    Qt, QObject, QEvent, QRectF, QLineF, QTimer, QPoint,
    pyqtSignal as Signal, pyqtSlot as Slot
)
from AnyQt.QtGui import QColor

import pyqtgraph as pg

from Orange.data import Table
from Orange.projection import FreeViz
from Orange.projection.freeviz import FreeVizModel
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.visualize.utils.component import OWGraphWithAnchors
from Orange.widgets.visualize.utils.plotutils import AnchorItem
from Orange.widgets.visualize.utils.widget import OWAnchorProjectionWidget


class AsyncUpdateLoop(QObject):
    """
    Run/drive an coroutine from the event loop.

    This is a utility class which can be used for implementing
    asynchronous update loops. I.e. coroutines which periodically yield
    control back to the Qt event loop.

    """
    Next = QEvent.registerEventType()

    #: State flags
    Idle, Running, Cancelled, Finished = 0, 1, 2, 3
    #: The coroutine has yielded control to the caller (with `object`)
    yielded = Signal(object)
    #: The coroutine has finished/exited (either with an exception
    #: or with a return statement)
    finished = Signal()

    #: The coroutine has returned (normal return statement / StopIteration)
    returned = Signal(object)
    #: The coroutine has exited with with an exception.
    raised = Signal(object)
    #: The coroutine was cancelled/closed.
    cancelled = Signal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.__coroutine = None
        self.__next_pending = False  # Flag for compressing scheduled events
        self.__in_next = False
        self.__state = AsyncUpdateLoop.Idle

    @Slot(object)
    def setCoroutine(self, loop):
        """
        Set the coroutine.

        The coroutine will be resumed (repeatedly) from the event queue.
        If there is an existing coroutine set it is first closed/cancelled.

        Raises an RuntimeError if the current coroutine is running.
        """
        if self.__coroutine is not None:
            self.__coroutine.close()
            self.__coroutine = None
            self.__state = AsyncUpdateLoop.Cancelled

            self.cancelled.emit()
            self.finished.emit()

        if loop is not None:
            self.__coroutine = loop
            self.__state = AsyncUpdateLoop.Running
            self.__schedule_next()

    @Slot()
    def cancel(self):
        """
        Cancel/close the current coroutine.

        Raises an RuntimeError if the current coroutine is running.
        """
        self.setCoroutine(None)

    def state(self):
        """
        Return the current state.
        """
        return self.__state

    def isRunning(self):
        return self.__state == AsyncUpdateLoop.Running

    def __schedule_next(self):
        if not self.__next_pending:
            self.__next_pending = True
            QTimer.singleShot(10, self.__on_timeout)

    def __next(self):
        if self.__coroutine is not None:
            try:
                rval = next(self.__coroutine)
            except StopIteration as stop:
                self.__state = AsyncUpdateLoop.Finished
                self.returned.emit(stop.value)
                self.finished.emit()
                self.__coroutine = None
            except BaseException as er:
                self.__state = AsyncUpdateLoop.Finished
                self.raised.emit(er)
                self.finished.emit()
                self.__coroutine = None
            else:
                self.yielded.emit(rval)
                self.__schedule_next()

    @Slot()
    def __on_timeout(self):
        assert self.__next_pending
        self.__next_pending = False
        if not self.__in_next:
            self.__in_next = True
            try:
                self.__next()
            finally:
                self.__in_next = False
        else:
            # warn
            self.__schedule_next()

    def customEvent(self, event):
        if event.type() == AsyncUpdateLoop.Next:
            self.__on_timeout()
        else:
            super().customEvent(event)


class OWFreeVizGraph(OWGraphWithAnchors):
    hide_radius = settings.Setting(0)

    @property
    def scaled_radius(self):
        return self.hide_radius / 100 + 1e-5

    def update_radius(self):
        self.update_circle()
        self.update_anchors()

    def set_view_box_range(self):
        self.view_box.setRange(QRectF(-1.05, -1.05, 2.1, 2.1))

    def closest_draggable_item(self, pos):
        points, *_ = self.master.get_anchors()
        if points is None or not len(points):
            return None
        mask = np.linalg.norm(points, axis=1) > self.scaled_radius
        xi, yi = points[mask].T
        distances = (xi - pos.x()) ** 2 + (yi - pos.y()) ** 2
        if len(distances) and np.min(distances) < self.DISTANCE_DIFF ** 2:
            return np.flatnonzero(mask)[np.argmin(distances)]
        return None

    def update_anchors(self):
        points, labels = self.master.get_anchors()
        if points is None:
            return
        r = self.scaled_radius
        if self.anchor_items is None:
            self.anchor_items = []
            for point, label in zip(points, labels):
                anchor = AnchorItem(line=QLineF(0, 0, *point), text=label)
                anchor.setVisible(np.linalg.norm(point) > r)
                anchor.setPen(pg.mkPen((100, 100, 100)))
                self.plot_widget.addItem(anchor)
                self.anchor_items.append(anchor)
        else:
            for anchor, point, label in zip(self.anchor_items, points, labels):
                anchor.setLine(QLineF(0, 0, *point))
                anchor.setText(label)
                anchor.setVisible(np.linalg.norm(point) > r)

    def update_circle(self):
        super().update_circle()
        if self.circle_item is not None:
            r = self.scaled_radius
            self.circle_item.setRect(QRectF(-r, -r, 2 * r, 2 * r))
            pen = pg.mkPen(QColor(Qt.lightGray), width=1, cosmetic=True)
            self.circle_item.setPen(pen)

    def _add_indicator_item(self, anchor_idx):
        x, y = self.anchor_items[anchor_idx].get_xy()
        dx = (self.view_box.childGroup.mapToDevice(QPoint(1, 0)) -
              self.view_box.childGroup.mapToDevice(QPoint(-1, 0))).x()
        self.indicator_item = MoveIndicator(x, y, 600 / dx)
        self.plot_widget.addItem(self.indicator_item)


class InitType(IntEnum):
    Circular, Random = 0, 1

    @staticmethod
    def items():
        return ["Circular", "Random"]


class OWFreeViz(OWAnchorProjectionWidget):
    MAX_ITERATIONS = 1000
    MAX_INSTANCES = 10000

    name = "FreeViz"
    description = "Displays FreeViz projection"
    icon = "icons/Freeviz.svg"
    priority = 240
    keywords = ["viz"]

    settings_version = 3
    initialization = settings.Setting(InitType.Circular)
    GRAPH_CLASS = OWFreeVizGraph
    graph = settings.SettingProvider(OWFreeVizGraph)

    class Error(OWAnchorProjectionWidget.Error):
        no_class_var = widget.Msg("Data has no target variable")
        not_enough_class_vars = widget.Msg(
            "Target variable is not at least binary")
        features_exceeds_instances = widget.Msg(
            "Number of features exceeds the number of instances.")
        too_many_data_instances = widget.Msg("Data is too large.")
        constant_data = widget.Msg("All data columns are constant.")
        not_enough_features = widget.Msg("At least two features are required")

    class Warning(OWAnchorProjectionWidget.Warning):
        removed_features = widget.Msg("Categorical features with more than"
                                      " two values are not shown.")

    def __init__(self):
        super().__init__()
        self._loop = AsyncUpdateLoop(parent=self)
        self._loop.yielded.connect(self.__set_projection)
        self._loop.finished.connect(self.__freeviz_finished)
        self._loop.raised.connect(self.__on_error)

    def _add_controls(self):
        self.__add_controls_start_box()
        super()._add_controls()
        self.gui.add_control(
            self._effects_box, gui.hSlider, "Hide radius:", master=self.graph,
            value="hide_radius", minValue=0, maxValue=100, step=10,
            createLabel=False, callback=self.__radius_slider_changed
        )

    def __add_controls_start_box(self):
        box = gui.vBox(self.controlArea, box=True)
        gui.comboBox(
            box, self, "initialization", label="Initialization:",
            items=InitType.items(), orientation=Qt.Horizontal,
            labelWidth=90, callback=self.__init_combo_changed)
        self.btn_start = gui.button(
            box, self, "Optimize", self.__toggle_start, enabled=False)

    @property
    def effective_variables(self):
        return [a for a in self.data.domain.attributes
                if a.is_continuous or a.is_discrete and len(a.values) == 2]

    def __radius_slider_changed(self):
        self.graph.update_radius()

    def __toggle_start(self):
        if self._loop.isRunning():
            self._loop.cancel()
            self.btn_start.setText("Optimize")
            self.progressBarFinished(processEvents=False)
        else:
            self._start()

    def __init_combo_changed(self):
        if self.data is None:
            return
        running = self._loop.isRunning()
        if running:
            self._loop.cancel()
        self.init_projection()
        self.graph.update_coordinates()
        self.commit()
        if running:
            self._start()

    def _start(self):
        def update_freeviz(anchors):
            while True:
                self.projection = self.projector(self.effective_data)
                _anchors = self.projector.components_.T
                self.projector.initial = _anchors
                yield _anchors
                if np.allclose(anchors, _anchors, rtol=1e-5, atol=1e-4):
                    return
                anchors = _anchors

        self.graph.set_sample_size(self.SAMPLE_SIZE)
        self._loop.setCoroutine(update_freeviz(self.projector.components_.T))
        self.btn_start.setText("Stop")
        self.progressBarInit()
        self.setBlocking(True)
        self.setStatusMessage("Optimizing")

    def __set_projection(self, _):
        # Set/update the projection matrix and coordinate embeddings
        self.progressBarAdvance(100. / self.MAX_ITERATIONS)
        self.graph.update_coordinates()

    def __freeviz_finished(self):
        self.graph.set_sample_size(None)
        self.btn_start.setText("Optimize")
        self.setStatusMessage("")
        self.setBlocking(False)
        self.progressBarFinished()
        self.commit()

    def __on_error(self, err):
        sys.excepthook(type(err), err, getattr(err, "__traceback__"))

    def check_data(self):
        def error(err):
            err()
            self.data = None

        super().check_data()
        if self.data is not None:
            class_var, domain = self.data.domain.class_var, self.data.domain
            if class_var is None:
                error(self.Error.no_class_var)
            elif class_var.is_discrete and len(np.unique(self.data.Y)) < 2:
                error(self.Error.not_enough_class_vars)
            elif len(self.data.domain.attributes) < 2:
                error(self.Error.not_enough_features)
            elif len(self.data.domain.attributes) > self.data.X.shape[0]:
                error(self.Error.features_exceeds_instances)
            elif not np.sum(np.std(self.data.X, axis=0)):
                error(self.Error.constant_data)
            elif np.sum(self.valid_data) > self.MAX_INSTANCES:
                error(self.Error.too_many_data_instances)
            else:
                if len(self.effective_variables) < len(domain.attributes):
                    self.Warning.removed_features()
        self.btn_start.setEnabled(self.data is not None)

    def set_data(self, data):
        super().set_data(data)
        if self.data is not None:
            self.init_projection()

    def init_projection(self):
        anchors = FreeViz.init_radial(len(self.effective_variables)) \
            if self.initialization == InitType.Circular \
            else FreeViz.init_random(len(self.effective_variables), 2)
        self.projector = FreeViz(scale=False, center=False,
                                 initial=anchors, maxiter=10)
        data = self.projector.preprocess(self.effective_data)
        self.projector.domain = data.domain
        self.projector.components_ = anchors.T
        self.projection = FreeVizModel(self.projector, self.projector.domain, 2)
        self.projection.pre_domain = data.domain
        self.projection.name = self.projector.name

    def get_coordinates_data(self):
        embedding = self.get_embedding()
        if embedding is None:
            return None, None
        valid_emb = embedding[self.valid_data]
        return valid_emb.T / (np.max(np.linalg.norm(valid_emb, axis=1)) or 1)

    def _manual_move(self, anchor_idx, x, y):
        self.projector.initial[anchor_idx] = [x, y]
        super()._manual_move(anchor_idx, x, y)

    def clear(self):
        super().clear()
        self._loop.cancel()

    @classmethod
    def migrate_settings(cls, _settings, version):
        if version < 3:
            if "radius" in _settings:
                _settings["graph"]["hide_radius"] = _settings["radius"]

    @classmethod
    def migrate_context(cls, context, version):
        if version < 3:
            values = context.values
            values["attr_color"] = values["graph"]["attr_color"]
            values["attr_size"] = values["graph"]["attr_size"]
            values["attr_shape"] = values["graph"]["attr_shape"]
            values["attr_label"] = values["graph"]["attr_label"]


class MoveIndicator(pg.GraphicsObject):
    def __init__(self, x, y, scene_size, parent=None):
        super().__init__(parent)
        self.arrows = [
            pg.ArrowItem(pos=(x - scene_size * 0.07 * np.cos(np.radians(ang)),
                              y + scene_size * 0.07 * np.sin(np.radians(ang))),
                         parent=self, angle=ang,
                         headLen=13, tipAngle=45,
                         brush=pg.mkColor(128, 128, 128))
            for ang in (0, 90, 180, 270)]

    def paint(self, painter, option, widget):
        pass

    def boundingRect(self):
        return QRectF()


if __name__ == "__main__":  # pragma: no cover
    data = Table("zoo")
    WidgetPreview(OWFreeViz).run(set_data=data, set_subset_data=data[::10])
