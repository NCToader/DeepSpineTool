# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:01:11 2019

@author: Marcos
"""
from PyQt5 import Qt
import numpy as np

from app.plugins.ui.nodeViewer._ui_matrix4 import Ui_matrix4Viewer_form


class Matrix4Viewer(Qt.QWidget):
    # =============================================================================
    # Definición de clases
    # =============================================================================
    class _LineEdit(Qt.QLineEdit):
        focusInSignal = Qt.pyqtSignal()
        focusOutSignal = Qt.pyqtSignal()

        def __init__(self, *args, coords=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.coords = coords

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
    # Definición de señales
    # =============================================================================

    matrixChangedSignal = Qt.pyqtSignal()

    # =============================================================================
    # Constructores
    # =============================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_matrix4Viewer_form()
        self.ui.setupUi(self)

        # editores
        self._editors = [[Matrix4Viewer._LineEdit(coords=(i, j))
                          for j in range(4)] for i in range(3)]

        for i, eds in enumerate(self._editors):
            for j, ed in enumerate(eds):
                ed.setValidator(Matrix4Viewer._Validator(ed))
                self.ui.matrix_table.setCellWidget(i, j, ed)
                ed.setFrame(False)
                ed.focusInSignal.connect(self._editionStarts)
                ed.focusOutSignal.connect(self._editionFinish)

        # matrices
        self._matrix = np.eye(4)
        self._showMatrix()

        self._currentNode = None
        self._currentAtrrib = None

    # =============================================================================
    # Metodos privados
    # ============================================================================= 

    def _showMatrix(self):
        for i, eds in enumerate(self._editors):
            for j, ed in enumerate(eds):
                val = self._matrix[i, j]
                ed.setText("{:.3g}".format(val))

    # =============================================================================
    # Slots    
    # =============================================================================

    @Qt.pyqtSlot()
    def _editionStarts(self):
        ed = self.sender()
        ed.setText(str(self._matrix[ed.coords]))

    @Qt.pyqtSlot()
    def _editionFinish(self):
        ed = self.sender()
        if not (ed.text() in ["", "-", "+"]) and \
                float(ed.text()) != self._matrix[ed.coords]:
            self._matrix[ed.coords] = float(ed.text())
            self.matrixChangedSignal.emit()
        #               if self._currentNode is not None:
        #                   self._currentAtrrib._set__(self._currentNode, self.matrix)

        self._showMatrix()

    def clear(self):
        self.matrix = np.eye(4)

    ##        if self._currentNode is not None:
    ##            self._currentNode.disconnectFromObjAttrib(self.nodeAttribChanged,
    ##                                                      self._currentAtrrib)
    ##        
    ##            self._currentNode = None
    ##            self._currentAtrrib = None
    #        
    #    
    ##    def connectNodeAttrib(self, node, attrib):
    ##        if self._currentObj is not None:
    ##            self.clear()
    ##            
    ##        self._currentNode = node
    ##        self._currentAtrrib = attrib
    ##        
    ##        node.connect2ObjAttrib(self.nodeAttribChanged, attrib)
    ##
    ##    def nodeAttribChanged(self, **kwargs):
    ##        nodeMatrix = self._currentAtrrib._get__(self._currentNode)
    ##        if not np.array_equal(self.matrix, nodeMatrix):
    ##            self.matrix = nodeMatrix

    @property
    def matrix(self):
        return np.copy(self._matrix)

    @matrix.setter
    def matrix(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError("Numpy array expected")

        if len(value.shape) != 2:
            raise ValueError("Matrix expected")

        if value.shape[0] < 3 and value.shape[1] < 4:
            raise ValueError("Wrong matrix dimensions")

        self._matrix[0:3, 0:4] = value[0:3, 0:4]

        self._showMatrix()


if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)
    ex = Matrix4Viewer()

    ex.matrix = np.eye(4)
    print(ex.matrix)

    ex.show()
    sys.exit(app.exec())
