# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:38:19 2019

@author: Marcos García
"""

from PyQt5 import Qt
import numbers as num


class LineEditEx(Qt.QLineEdit):
    valueChangedSignal = Qt.pyqtSignal()
    focusInSignal = Qt.pyqtSignal()
    focusOutSignal = Qt.pyqtSignal()

    class _DValidator(Qt.QDoubleValidator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.setNotation(Qt.QDoubleValidator.ScientificNotation)

        def validate(self,
                     text, pos):
            state, _, _ = super().validate(text, pos)

            if text in ["", "-", "+"]:
                state = Qt.QValidator.Acceptable

            return state, text, pos

    class _IValidator(Qt.QIntValidator):
        def validate(self, text, pos):
            state, _, _ = super().validate(text, pos)

            if text in ["", "-", "+"]:
                state = Qt.QValidator.Acceptable

            return state, text, pos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clear()

        self.focusOutSignal.connect(self._editionFinish)
        self.focusInSignal.connect(self._editionStarts)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.focusInSignal.emit()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.focusOutSignal.emit()

    def clear(self):
        self.setStringFormat()
        self.value = ""
        self.editable = True

    def setIntFormat(self, mn=None, mx=None):
        if mn is None and mx is None:
            self.setValidator(LineEditEx._IValidator())
        elif mn is None:
            self.setValidator(LineEditEx._IValidator(top=mx))
        elif mx is None:
            self.setValidator(LineEditEx._IValidator(bottom=mn))
        else:
            self.setValidator(LineEditEx._IValidator(bottom=mn, top=mx))

        self._type = int
        self._converterToType = lambda s: int(s)
        self._converterToStr = lambda v: str(v)
        self._validator = lambda v: isinstance(v, num.Integral)

    def setFloatFormat(self, mn=None, mx=None):
        if mn is None and mx is None:
            self.setValidator(LineEditEx._DValidator())
        elif mn is None:
            self.setValidator(LineEditEx._DValidator(top=mx))
        elif mx is None:
            self.setValidator(LineEditEx._DValidator(bottom=mn))
        else:
            self.setValidator(LineEditEx._DValidator(bottom=mn, top=mx))
        self._type = float
        self._converterToType = lambda s: float(s)
        self._converterToStr = lambda v: "{:.3g}".format(v)
        self._validator = lambda v: isinstance(v, num.Real)

    def setStringFormat(self):
        self.setValidator(None)
        self._type = None
        self._converterToType = None
        self._converterToStr = None
        self._validator = None

    @property
    def editable(self):
        return self._editable

    @editable.setter
    def editable(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._editable = value
        self.setReadOnly(not value)

    def _editionFinish(self):
        if self._isValid():
            str_ = self._getStrig()

            if self._converterToType is not None:
                val = self._converterToType(str_)
            else:
                val = str_

            if self.validator() is not None:
                if self.validator().bottom() is not None:
                    if val < self.validator().bottom():
                        val = self.validator().bottom()
                elif self.validator().top() is not None:
                    if val > self.validator().top():
                        val = self.validator().top()

            if self.value != val:
                self.value = val
                self.valueChangedSignal.emit()
            else:
                self.value = self._val

    def _editionStarts(self):
        if self._isValid():
            self.setText(str(self._val))

    def _isValid(self):
        str_ = self._getStrig()

        if self._type is not None:
            if issubclass(self._type, num.Number):
                if str_ in ["", "-", "+"]: return False

        result = True

        if self._validator is not None:
            if self._converterToType is not None:
                val = self._converterToType(str_)
            else:
                val = str_
            result = result and self._validator(val)

        return result

    @property
    def value(self):
        if self._validator is not None:
            if not self._validator(self._val):
                return None
        return self._val

    @value.setter
    def value(self, value):

        if self._validator is not None:
            if not self._validator(value):
                v = self._val
                if self._converterToStr:
                    v = self._converterToStr(v)
                self.setText(v)

        v = value
        if self._converterToStr:
            v = self._converterToStr(v)

        self._val = value
        self.setText(v)

    def _getStrig(self):
        return self.text()
