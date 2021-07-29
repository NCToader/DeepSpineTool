# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:21:33 2019

@author: Marcos

#!Todo: Reutilizar _LineEdit
#!Todo: No me gustán esta clases
"""

from PyQt5 import Qt
import numbers as num
from typing import Iterable

from app.core.model import SceneProperty

from app.plugins.ui.nodeViewer._ui_lineEdit import Ui_lineEdit_widget


class LineEdit(Qt.QWidget):
    # =============================================================================
    # Definición de clases
    # =============================================================================
    class _LineEdit(Qt.QLineEdit):
        focusInSignal = Qt.pyqtSignal()
        focusOutSignal = Qt.pyqtSignal()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def focusInEvent(self, e):
            super().focusInEvent(e)
            self.focusInSignal.emit()

        def focusOutEvent(self, e):
            super().focusOutEvent(e)
            self.focusOutSignal.emit()

    class _Validator(Qt.QDoubleValidator):
        def __init__(self, *args, coords=None, **kwargs):
            super().__init__(*args, **kwargs)

            self.setNotation(Qt.QDoubleValidator.ScientificNotation)

        def validate(self, text, pos):
            state, _, _ = super().validate(text, pos)

            if text in ["", "-", "+"]:
                state = Qt.QIntValidator.Acceptable

            return state, text, pos

    # =============================================================================
    # Definición de señales y Globales
    # =============================================================================

    valueChangedSignal = Qt.pyqtSignal()

    vaildTypes = [num.Number, (str)]
    qvalidators = [_Validator, None]

    #    val2string = [lambda v: return "{:.3g}".format(v), str]
    #    string2val = [lambda t, v: return t(v) if t != num.Number else float(v),\
    #                  return v]

    # =============================================================================
    # Constructores
    # =============================================================================

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_lineEdit_widget()
        self.ui.setupUi(self)

        le = LineEdit._LineEdit()
        self.layout().replaceWidget(self.ui.lineEdit, le)
        self.ui.lineEdit.deleteLater()
        self.ui.lineEdit = le
        le.focusOutSignal.connect(self._editionFinish)

        self.clear()

    def _editionFinish(self):
        if self._isValid() and self._string != self.value:
            self._string = self.value
            self.valueChangedSignal.emit()
        else:
            self.value = self._string

    def _isValid(self):
        val = self.value

        if self._type is not None:
            if issubclass(self._type, num.Number):
                if val in ["", "-", "+"]: return False

        result = True

        if self._validator is not None:
            result = result and self._validator(self._obj, val)

        if self._typeValidator is not None:
            result = result and self._typeValidator(self._obj, val)

        return result

    @staticmethod
    def getValidAttribType(obj, attr):
        if not isinstance(attr, SceneProperty):
            raise TypeError("SceneProperty expected")

        atypes = attr.getValidType()

        for t, qv in zip(LineEdit.vaildTypes, LineEdit.qvalidators):
            if isinstance(atypes, Iterable):
                if any(issubclass(at, t) for at in atypes):
                    return t, qv
            else:
                if atypes is not None and issubclass(atypes, t):
                    return t, qv

        return None

    def setAttrib(self, obj, attr):
        t, qv = self.getValidAttribType(obj, attr)
        if t is not None:
            self._type = t
            self._validator = attr.validateValue
            self._typeValidator = attr.validateType
            self._obj = obj
            self._attr = attr
            self.editable = not attr.readOnly()
            if qv is not None:
                self.ui.lineEdit.setValidator(qv(self))
            self.value = attr.getValue(obj)
            self.label = attr.getName().title()

    def getAttrib(self):
        return self._attr

    def clear(self):
        self.ui.lineEdit.setValidator(None)
        self.editable = True

        self.value = ""

        self._type = None
        self._validator = None
        self._typeValidator = None
        self._obj = None
        self._attr = None

    @property
    def label(self):
        return self.ui.attr_label.text()

    @label.setter
    def label(self, value):
        self.ui.attr_label.setText(value)

    @property
    def value(self):
        s = self.ui.lineEdit.text()
        if self._type is not None:
            s = self._type(s) if self._type != num.Number else float(s)

        return s

    @value.setter
    def value(self, value):
        v = "{:.3g}".format(value) if isinstance(value, num.Number) else \
            str(value)

        self.ui.lineEdit.setText(v)
        self._string = v

    @property
    def editable(self):
        return self._editable

    @editable.setter
    def editable(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._editable = value
        self.ui.lineEdit.setReadOnly(not value)


if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)

    ex = LineEdit()
    ex.show()
    ex.label = 'Pajaro'
    ex.value = 'Pio'

    sys.exit(app.exec())
