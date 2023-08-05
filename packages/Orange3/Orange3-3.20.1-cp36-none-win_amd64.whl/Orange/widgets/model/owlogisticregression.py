from itertools import chain
import numpy as np
from AnyQt.QtCore import Qt

from Orange.data import Table, Domain, ContinuousVariable, StringVariable
from Orange.classification.logistic_regression import LogisticRegressionLearner
from Orange.widgets import settings, gui
from Orange.widgets.utils.owlearnerwidget import OWBaseLearner
from Orange.widgets.utils.signals import Output
from Orange.widgets.utils.widgetpreview import WidgetPreview


class OWLogisticRegression(OWBaseLearner):
    name = "Logistic Regression"
    description = "The logistic regression classification algorithm with " \
                  "LASSO (L1) or ridge (L2) regularization."
    icon = "icons/LogisticRegression.svg"
    replaces = [
        "Orange.widgets.classify.owlogisticregression.OWLogisticRegression",
    ]
    priority = 60
    keywords = []

    LEARNER = LogisticRegressionLearner

    class Outputs(OWBaseLearner.Outputs):
        coefficients = Output("Coefficients", Table, explicit=True)

    penalty_type = settings.Setting(1)
    C_index = settings.Setting(61)

    C_s = list(chain(range(1000, 200, -50),
                     range(200, 100, -10),
                     range(100, 20, -5),
                     range(20, 0, -1),
                     [x / 10 for x in range(9, 2, -1)],
                     [x / 100 for x in range(20, 2, -1)],
                     [x / 1000 for x in range(20, 0, -1)]))
    dual = False
    tol = 0.0001
    fit_intercept = True
    intercept_scaling = 1.0

    penalty_types = ("Lasso (L1)", "Ridge (L2)")
    penalty_types_short = ["l1", "l2"]

    def add_main_layout(self):
        box = gui.widgetBox(self.controlArea, box=True)
        self.penalty_combo = gui.comboBox(
            box, self, "penalty_type", label="Regularization type: ",
            items=self.penalty_types, orientation=Qt.Horizontal,
            addSpace=4, callback=self.settings_changed)
        gui.widgetLabel(box, "Strength:")
        box2 = gui.hBox(gui.indentedBox(box))
        gui.widgetLabel(box2, "Weak").setStyleSheet("margin-top:6px")
        self.c_slider = gui.hSlider(
            box2, self, "C_index", minValue=0, maxValue=len(self.C_s) - 1,
            callback=lambda: (self.set_c(), self.settings_changed()),
            createLabel=False)
        gui.widgetLabel(box2, "Strong").setStyleSheet("margin-top:6px")
        box2 = gui.hBox(box)
        box2.layout().setAlignment(Qt.AlignCenter)
        self.c_label = gui.widgetLabel(box2)
        self.set_c()

    def set_c(self):
        self.strength_C = self.C_s[self.C_index]
        fmt = "C={}" if self.strength_C >= 1 else "C={:.3f}"
        self.c_label.setText(fmt.format(self.strength_C))

    def create_learner(self):
        penalty = self.penalty_types_short[self.penalty_type]
        return self.LEARNER(
            penalty=penalty,
            dual=self.dual,
            tol=self.tol,
            C=self.strength_C,
            fit_intercept=self.fit_intercept,
            intercept_scaling=self.intercept_scaling,
            preprocessors=self.preprocessors
        )

    def update_model(self):
        super().update_model()
        coef_table = None
        if self.model is not None:
            coef_table = create_coef_table(self.model)
        self.Outputs.coefficients.send(coef_table)

    def get_learner_parameters(self):
        return (("Regularization", "{}, C={}".format(
            self.penalty_types[self.penalty_type], self.C_s[self.C_index])),)


def create_coef_table(classifier):
    i = classifier.intercept
    c = classifier.coefficients
    if c.shape[0] > 2:
        values = [classifier.domain.class_var.values[int(i)] for i in classifier.used_vals[0]]
    else:
        values = [classifier.domain.class_var.values[int(classifier.used_vals[0][1])]]
    domain = Domain([ContinuousVariable(value, number_of_decimals=7)
                     for value in values], metas=[StringVariable("name")])
    coefs = np.vstack((i.reshape(1, len(i)), c.T))
    names = [[attr.name] for attr in classifier.domain.attributes]
    names = [["intercept"]] + names
    names = np.array(names, dtype=object)
    coef_table = Table.from_numpy(domain, X=coefs, metas=names)
    coef_table.name = "coefficients"
    return coef_table


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWLogisticRegression).run(Table("zoo"))
