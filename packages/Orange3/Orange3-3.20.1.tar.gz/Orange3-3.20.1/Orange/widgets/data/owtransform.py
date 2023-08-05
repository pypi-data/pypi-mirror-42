import numpy as np

from Orange.data import Table, Domain
from Orange.preprocess.preprocess import Preprocess, Discretize
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.sql import check_sql_input
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg


class OWTransform(OWWidget):
    name = "Transform"
    description = "Transform data table."
    icon = "icons/Transform.svg"
    priority = 2110
    keywords = []

    retain_all_data = Setting(False)

    class Inputs:
        data = Input("Data", Table, default=True)
        preprocessor = Input("Preprocessor", Preprocess)

    class Outputs:
        transformed_data = Output("Transformed Data", Table)

    class Error(OWWidget.Error):
        pp_error = Msg("An error occurred while transforming data.\n{}")

    resizing_enabled = False
    want_main_area = False

    def __init__(self):
        super().__init__()
        self.data = None
        self.preprocessor = None
        self.transformed_data = None

        info_box = gui.widgetBox(self.controlArea, "Info")
        self.input_label = gui.widgetLabel(info_box, "")
        self.preprocessor_label = gui.widgetLabel(info_box, "")
        self.output_label = gui.widgetLabel(info_box, "")
        self.set_input_label_text()
        self.set_preprocessor_label_text()

        self.retain_all_data_cb = gui.checkBox(
            self.controlArea, self, "retain_all_data", label="Retain all data",
            callback=self.apply
            )

    def set_input_label_text(self):
        text = "No data on input."
        if self.data is not None:
            text = "Input data with {:,} instances and {:,} features.".format(
                len(self.data),
                len(self.data.domain.attributes))
        self.input_label.setText(text)

    def set_preprocessor_label_text(self):
        text = "No preprocessor on input."
        if self.transformed_data is not None:
            text = "Preprocessor {} applied.".format(self.preprocessor)
        elif self.preprocessor is not None:
            text = "Preprocessor {} on input.".format(self.preprocessor)
        self.preprocessor_label.setText(text)

    def set_output_label_text(self):
        text = ""
        if self.transformed_data:
            text = "Output data includes {:,} features.".format(
                len(self.transformed_data.domain.attributes))
        self.output_label.setText(text)

    @Inputs.data
    @check_sql_input
    def set_data(self, data):
        self.data = data
        self.set_input_label_text()

    @Inputs.preprocessor
    def set_preprocessor(self, preprocessor):
        self.preprocessor = preprocessor

    def handleNewSignals(self):
        self.apply()

    def apply(self):
        self.clear_messages()
        self.transformed_data = None
        if self.data is not None and self.preprocessor is not None:
            try:
                self.transformed_data = self.preprocessor(self.data)
            except Exception as ex:   # pylint: disable=broad-except
                self.Error.pp_error(ex)

        if self.retain_all_data:
            self.Outputs.transformed_data.send(self.merge_data())
        else:
            self.Outputs.transformed_data.send(self.transformed_data)

        self.set_preprocessor_label_text()
        self.set_output_label_text()

    def merge_data(self):
        attributes = getattr(self.data.domain, 'attributes')
        cls_vars = getattr(self.data.domain, 'class_vars')
        metas_v = getattr(self.data.domain, 'metas')\
            + getattr(self.transformed_data.domain, 'attributes')
        domain = Domain(attributes, cls_vars, metas_v)
        X = self.data.X
        Y = self.data.Y
        metas = np.hstack((self.data.metas, self.transformed_data.X))
        table = Table.from_numpy(domain, X, Y, metas)
        table.name = getattr(self.data, 'name', '')
        table.attributes = getattr(self.data, 'attributes', {})
        table.ids = self.data.ids
        return table

    def send_report(self):
        if self.preprocessor is not None:
            self.report_items("Settings",
                              (("Preprocessor", self.preprocessor),))
        if self.data is not None:
            self.report_data("Data", self.data)
        if self.transformed_data is not None:
            self.report_data("Transformed data", self.transformed_data)


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWTransform).run(
        set_data=Table("iris"),
        set_preprocessor=Discretize())
