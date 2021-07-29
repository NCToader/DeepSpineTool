# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:21:50 2019

@author: Marcos
"""

from PyQt5 import Qt
import enum
from typing import Iterable

from app.core.model import SceneProperty

from app.plugins.ui.nodeViewer._ui_comboBox import Ui_comboBox_widget


class ComboBox(Qt.QWidget):
    ## =============================================================================
    ## Definición de clases
    ## =============================================================================
    #    class _ComboBox(Qt.QComboBox):
    #        focusInSignal = Qt.pyqtSignal()
    #        focusOutSignal = Qt.pyqtSignal()
    #        
    #        def __init__(self, *args, **kwargs):
    #            super().__init__(*args,**kwargs)
    #            
    #        def focusInEvent(self, e):
    #            super().focusInEvent(e)
    #            self.focusInSignal.emit()
    #            
    #        def focusOutEvent(self, e):
    #            super().focusOutEvent(e)
    #            self.focusOutSignal.emit()

    # =============================================================================
    # Definición de señales y Globales
    # =============================================================================
    valueChangedSignal = Qt.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_comboBox_widget()
        self.ui.setupUi(self)

        #        cmb = ComboBox._ComboBox()
        #        self.layout().replaceWidget(self.ui.comboBox, cmb)
        #        self.ui.comboBox.deleteLater()
        #        self.ui.comboBox = cmb
        self.ui.comboBox.currentIndexChanged.connect(self._editionFinish)

        self.clear()

    @Qt.pyqtSlot()
    def _editionFinish(self):
        idx = self.ui.comboBox.currentIndex()
        if self._oldIdx != idx and self._isValid(self.value):
            self._oldIdx = idx
            self.valueChangedSignal.emit()
        else:
            self.ui.comboBox.setCurrentIndex(self._oldIdx)

    def _isValid(self, value):
        if not isinstance(value, self._type):
            return False

        result = True

        if self._validator is not None:
            result = result and self._validator(self._obj, value)

        if self._typeValidator is not None:
            result = result and self._typeValidator(self._obj, value)

        return result

    @staticmethod
    def getValidAttribType(obj, attr):
        if not isinstance(attr, SceneProperty):
            raise TypeError("SceneProperty expected")

        atypes = attr.getValidType()

        if isinstance(atypes, Iterable):
            for at in atypes:
                if issubclass(at, enum.Enum):
                    return at
        else:
            if atypes is not None and issubclass(atypes, enum.Enum):
                return atypes

        return None

    def setAttrib(self, obj, attr):
        t = self.getValidAttribType(obj, attr)

        if t is not None:
            self._type = t
            self._validator = attr.validateValue
            self._typeValidator = attr.validateType
            self._obj = obj
            self._attr = attr

            self._acceptedValues = [vt for vt in t]

            for vt in t:
                self.ui.comboBox.addItem(vt.name)

            self.value = attr.getValue(obj)
            self.label = attr.getName().title()
            self.ui.comboBox.setDisabled(attr.readOnly())

    def getAttrib(self):
        return self._attr

    def clear(self):
        self._acceptedValues = []
        self._type = None
        self._validator = None
        self._typeValidator = None
        self._obj = None
        self._attr = None
        self._oldIdx = -1

        self.ui.comboBox.clear()
        self.ui.comboBox.setDisabled(True)

    @property
    def label(self):
        return self.ui.label.text()

    @label.setter
    def label(self, value):
        self.ui.label.setText(value)

    @property
    def value(self):
        if self._type is not None:
            idx = self.ui.comboBox.currentIndex()
            return self._acceptedValues[idx]

        return None

    @value.setter
    def value(self, value):
        if value in self._acceptedValues and self._isValid(value):
            idx = self._acceptedValues.index(value)
            if self._oldIdx != idx:
                self._oldIdx = idx
                self.ui.comboBox.setCurrentIndex(idx)


#    @property
#    def editable(self):
#        return self._editable
#    
#    @editable.setter
#    def editable(self, value):
#        if not isinstance(value, bool):
#            raise TypeError("Boolean expected")
#        
#        self._editable = value
#        self.ui.comboBox.setEditable(value)


if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)

    ex = ComboBox()
    ex.show()

    sys.exit(app.exec())
