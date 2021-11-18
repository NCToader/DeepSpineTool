# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:06:15 2019

@author: Marcos
"""

import numpy as np
from PyQt5 import Qt

from app.core import ui as mw
from app.core.utils import SingletonDecorator
from app.plugins.ui import sceneManagerUi as scm
from app.plugins.ui.nodeViewer._comboBox import ComboBox
from app.plugins.ui.nodeViewer._lineEdit import LineEdit
from app.plugins.ui.nodeViewer._matrixViewer import Matrix4Viewer
from app.plugins.ui.nodeViewer._ui_nodeViewer import Ui_nodeViewer_form
from app.plugins.utils.inspectors import getClassSCPAttribs


# from app.core import model as sc
# from app.core.model import SceneNode

class NodeViewerWidget(Qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_nodeViewer_form()
        self.ui.setupUi(self)

        # Interfaz Nombre
        self.ui.name_lineEditWidget = LineEdit()
        self.ui.name_lineEditWidget.label = "Name: "
        #        self.ui.name_lineEditWidget.value = ""
        self.ui.name_lineEditWidget.valueChangedSignal.connect(
            self._uiLineEditUpdated)

        self.ui.widgets_layout.insertWidget(1, (self.ui.name_lineEditWidget))

        # Interfaz Matriz Local Transform
        self.ui.localTransform_matrixViewer = Matrix4Viewer()
        self.ui.localTransform_layout.addItem(Qt.QSpacerItem(5, 0))
        self.ui.localTransform_layout.addWidget(
            self.ui.localTransform_matrixViewer)
        self.ui.localTransform_layout.addItem(Qt.QSpacerItem(0, 0,
                                                             hPolicy=Qt.QSizePolicy.Expanding))

        self.ui.localTransform_matrixViewer.matrixChangedSignal.connect(
            self._uiMatrixUpdated)

        # Interfaz Matriz Global Transform
        self.ui.globalTransform_matrixViewer = Matrix4Viewer()
        self.ui.globalTransform_layout.addWidget(
            self.ui.globalTransform_matrixViewer)
        self.ui.globalTransform_layout.addItem(Qt.QSpacerItem(0, 0,
                                                              hPolicy=Qt.QSizePolicy.Expanding))

        self.ui.globalTransform_matrixViewer.matrixChangedSignal.connect(
            self._uiMatrixUpdated)

        # Se deshabilita el interfaz
        self.setEnabled(False)

        self._smUI = scm.SceneManagerUI()
        self._smUI.currentItemChangedSignal.connect(self._currentNodeUpdated)

        self._currentNode = None
        self._attr2Widget = dict()

    def setNode(self, node):
        self.clear()
        self.setEnabled(True)

        self._currentNode = node

        self.ui.globalTransform_matrixViewer.matrix = node.globalTransform
        self.ui.localTransform_matrixViewer.matrix = node.transform

        self.ui.name_lineEditWidget.setAttrib(node, getattr(type(node), "name"))

        self.ui.nodeType_lineEdit.setText(
            " <<< ".join(node.getClassNameHierarchy()))

        node.connect2Obj(self._nodeChange)

        # Se añaden el resto de atributos
        #        attrList = getClassSCPAttribs(node,
        #          notHas = ["transform","globalTransform","name"])
        attrList = getClassSCPAttribs(node,
                                      notHas=["transform", "globalTransform", "name"])

        for a in attrList:
            #            attr = getattr(type(node),a[0])
            attr = a[1]
            if ComboBox.getValidAttribType(node, attr) is not None:
                cmb = ComboBox()
                cmb.setAttrib(node, attr)
                cmb.valueChangedSignal.connect(self._uiComboBoxUpdated)
                self.ui.widgets_layout.addWidget(cmb)
                self._attr2Widget[attr] = cmb

            elif LineEdit.getValidAttribType(node, attr) is not None:
                le = LineEdit()
                le.setAttrib(node, attr)
                le.valueChangedSignal.connect(self._uiLineEditUpdated)
                self.ui.widgets_layout.addWidget(le)
                self._attr2Widget[attr] = le

    def clear(self):
        self._currentNode = None

        self.ui.globalTransform_matrixViewer.clear()
        self.ui.localTransform_matrixViewer.clear()
        self.ui.nodeType_lineEdit.clear()
        self.ui.name_lineEditWidget.clear()

        for w in self._attr2Widget.values():
            self.ui.widgets_layout.removeWidget(w)
            w.deleteLater()

        self._attr2Widget.clear()

        self.setEnabled(False)

    @Qt.pyqtSlot()
    def _currentNodeUpdated(self):
        self.clear()

        node = self._smUI.currentNode
        if node is not None:
            self.setNode(node)

    @Qt.pyqtSlot()
    def _uiMatrixUpdated(self):
        if self._currentNode is not None:
            matrix = self.sender()
            if matrix == self.ui.localTransform_matrixViewer:
                self._currentNode.transform = \
                    matrix.matrix
            elif matrix == self.ui.globalTransform_matrixViewer:
                obj = self._currentNode
                oldGlobal = obj.globalTransform  # oG
                oldLocal = obj.transform  # oL
                newGlobal = matrix.matrix  # nG

                # pG * oL = oG ----> pG = oG * oL^{-1}
                # nG = pG * nL ----> nL = pG^{-1} * nG
                # nL = oL * oG^{1} * nG
                parentInv = oldLocal.dot(np.linalg.inv(oldGlobal))
                newLocal = parentInv.dot(newGlobal)
                self._currentNode.transform = newLocal

    @Qt.pyqtSlot()
    def _uiLineEditUpdated(self):
        if self._currentNode is not None:
            le = self.sender()
            if le == self.ui.name_lineEditWidget:
                self._currentNode.name = le.value
            else:
                attr = le.getAttrib()
                attr.setValue(self._currentNode, le.value)

    @Qt.pyqtSlot()
    def _uiComboBoxUpdated(self):
        if self._currentNode is not None:
            cmb = self.sender()
            attr = cmb.getAttrib()
            attr.setValue(self._currentNode, cmb.value)

    def _nodeChange(self, obj=None, attrib=None, **kwargs):
        if attrib == type(obj).transform:
            self.ui.localTransform_matrixViewer.matrix = obj.transform
        elif attrib == type(obj).globalTransform:
            self.ui.globalTransform_matrixViewer.matrix = obj.globalTransform
        elif attrib == type(obj).name:
            self.ui.name_lineEditWidget.value = obj.name
        if attrib in self._attr2Widget:

            w = self._attr2Widget.get(attrib, None)
            if w is not None:
                if isinstance(w, LineEdit): w.value = attrib.getValue(obj)
                if isinstance(w, ComboBox): w.value = attrib.getValue(obj)


@SingletonDecorator
class NodeViewerManager():
    def __init__(self):
        self._mw = mw.MainWindow()
        # !todo: Debería ser una propiedad
        self.nvw = NodeViewerWidget(self._mw)
        dock = self._mw.createDockableWidget(self.nvw, "Node Viewer",
                                             dockAreaId=mw.DockAreaId.Right)

        dock.hide()


def init():
    NodeViewerManager()

# if __name__ == '__main__':
#     import sys
#     app = Qt.QApplication(sys.argv)
#     ex = NodeViewerWidget()
#     ex.show()
#     sys.exit(app.exec())
