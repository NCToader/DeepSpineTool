# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 18:56:17 2019

@author: Marcos

https://www.youtube.com/watch?v=m_LXqG8VoDA&t=2s
!todo: mantener la transformación global si hay algun flag que lo indica
"""

#  This file is part of DeepSpineTool
#  Copyright (C) 2021 VG-Lab (Visualization & Graphics Lab), Universidad Rey Juan Carlos
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import Qt
from typing import Iterable

from app.core.utils import SingletonDecorator
from app.core import ui as mw
from app.core import model as sc

from app.plugins.ui import loaderManager as lm
from app.plugins.ui.sceneManagerUi.ui_SceneManagerTree import Ui_Form_SceneManager
from app.plugins.ui import iconManager as ic


class SceneManagerTree(Qt.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form_SceneManager()
        self.ui.setupUi(self)

        scene = sc.Scene()
        # Interface Setup

        self.ui.treeWidget.setHeaderLabels(["Name", "Node Type"])
        self.ui.treeWidget.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
        self.ui.treeWidget.setColumnHidden(1, True)
        self.ui.treeWidget.setAcceptDrops(True)
        self.ui.treeWidget.setDragEnabled(True)
        self.ui.treeWidget.setDragDropMode(
            Qt.QAbstractItemView.InternalMove)
        self.ui.treeWidget.setSelectionMode(
            Qt.QAbstractItemView.ExtendedSelection)

        # Internal data types
        self._nodes2Items = dict()

        # Creación del nodo escena
        self._sceneItem = self._createItem(self.ui.treeWidget,
                                           scene.name,
                                           scene.getClassName(),
                                           ic.NodeIconManager().getNodeIcon(
                                               scene.getClass()))
        self._sceneItem.setFlags(self._sceneItem.flags()
                                 & ~Qt.Qt.ItemIsDragEnabled)
        root = self.ui.treeWidget.invisibleRootItem()
        root.setFlags(root.flags() & ~Qt.Qt.ItemIsDropEnabled)

        #        self.ui.treeWidget.addTopLevelItem(self._sceneItem)

        # Conexiones con el modelo de datos
        scene.connect2Scene(self.sceneChanged)

        sc.SceneNode.name.connect2Attrib(self.nodeNameChanged)

        # Conexiones con el interfaz
        #        self.ui.pushButton_AddNode.clicked.connect(self.addNode)
        self.ui.pushButton_AddNode.setMenu(lm.LoaderManager().menu)
        lm.LoaderManager().createNodeCB = self._addNode

        self.ui.pushButton_RemoveNode.clicked.connect(self.removeNode)
        self.ui.checkBox_ShowType.toggled.connect(self.hideTypeCol)
        self.ui.treeWidget.itemDoubleClicked.connect(self.startItemEdition)
        self.ui.treeWidget.itemChanged.connect(self.itemChanged)

        self.ui.treeWidget.dropEvent = self.dropEvent(
            self.ui.treeWidget.dropEvent)

    # =============================================================================
    # Slots
    # =============================================================================
    @Qt.pyqtSlot()
    def removeNode(self):
        items = self.ui.treeWidget.selectedItems()

        if len(items) == 0:
            # https://www.qtcentre.org/threads/41269-disable-close-button-in-QMessageBox
            # https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
            mw.MainWindow().warningMsg("No node selected")
            return

        elif self._sceneItem in items:
            mw.MainWindow().warningMsg("Scene can not be removed")
            return

        for i in items:
            sc.Scene().removeSceneNode(i.node)

    # @Qt.pyqtSlot()
    def _addNode(self, cb):
        items = self.ui.treeWidget.selectedItems()

        if len(items) > 1:
            mw.MainWindow().warningMsg("More than one parent node selected")
            return
        elif len(items) == 0:
            parentNode = None
        else:
            item = items[0]
            parentNode = None if item == self._sceneItem else item.node

        value = cb()
        if value is not None:
            if isinstance(value, Iterable):
                for n in value:
                    #                    if isinstance(value, sc.SceneNode):
                    sc.Scene().addNode2Parent(n, parent=parentNode)
            #            elif isinstance(value, sc.SceneNode):
            else:
                sc.Scene().addNode2Parent(value, parent=parentNode)

    @Qt.pyqtSlot(bool)
    def hideTypeCol(self, value):
        self.ui.treeWidget.setColumnHidden(1, not value)

    @Qt.pyqtSlot(Qt.QTreeWidgetItem, int)
    def startItemEdition(self, item, col):
        if col == 0:
            self.ui.treeWidget.editItem(item, col)

    @Qt.pyqtSlot(Qt.QTreeWidgetItem, int)
    def itemChanged(self, item, col):
        if col == 0:
            if self._sceneItem == item:
                node = sc.Scene()
            elif hasattr(item, "node"):
                node = item.node
            else:
                node = None

            if node is not None and node.name != item.text(col):
                node.name = item.text(col)
                if item.parent() is not None:
                    item.parent().sortChildren(0, Qt.Qt.AscendingOrder)

    # =============================================================================
    # Redefinición de funciones en tiempo de ejecución
    # =============================================================================
    def dropEvent(self, func):
        def dropEventWrap(event):
            items = self.ui.treeWidget.selectedItems()
            oldParents = [i.parent() for i in items]

            func(event)

            newParents = [i.parent() for i in items]

            for op, np, i in zip(oldParents, newParents, items):
                if op != np:
                    if np == self._sceneItem:
                        pNode = None
                    else:
                        pNode = np.node

                    sc.Scene().addNode2Parent(i.node, parent=pNode)

                np.sortChildren(0, Qt.Qt.AscendingOrder)

        return dropEventWrap

    # =============================================================================
    #         Conexiones con el modelo de datos
    # =============================================================================
    def nodeNameChanged(self, obj=None, **kwargs):
        if obj in self._nodes2Items:
            self._nodes2Items[obj].setText(0, obj.name)

            # !todo: Pensar bien cuales necesitan ordenación
            p = self._nodes2Items[obj].parent()
            if p is not None:
                p.sortChildren(0, Qt.Qt.AscendingOrder)

    def sceneChanged(self, op=None,
                     node=None,
                     oldParent=None,
                     newParent=None,
                     name=None,
                     **kwargs):

        if (op == 'nodeCreated'):
            if node is None: return

            if (newParent == sc.Scene()):
                parentItem = self._sceneItem
            else:
                parentItem = self._nodes2Items[newParent]

            item = self._createItem(parentItem,
                                    node.name,
                                    node.getClassName(),
                                    ic.NodeIconManager().getNodeIcon(
                                        node.getClass()))
            item.node = node

            self._nodes2Items[node] = item

            p = item.parent()
            if p is not None:
                p.sortChildren(0, Qt.Qt.AscendingOrder)

        elif (op == "nodeMoved"):
            if node is None and \
                    newParent is None and \
                    oldParent is None: return
            if oldParent == newParent: return

            item = self._nodes2Items[node]
            if newParent is sc.Scene():
                newItem = self._sceneItem
            else:
                newItem = self._nodes2Items[newParent]
            if item.parent() == newItem: return

            item.parent().removeChild(item)
            newItem.addChild(item)

            item.parent().sortChildren(0, Qt.Qt.AscendingOrder)

            p = item.parent()
            if p is not None:
                p.sortChildren(0, Qt.Qt.AscendingOrder)
        #
        #            if oldParent is sc.Scene(): oldItem = self._sceneItem
        #            else: oldItem = self._node2Items[oldParent]
        elif (op == "nodeRemoved"):
            if node is None: return

            item = self._nodes2Items.pop(node)
            item.parent().removeChild(item)

        elif (op == 'nameChanged'):
            self._sceneItem.setText(0, sc.Scene().name)

    # =============================================================================
    # Funciones privadas
    # =============================================================================

    def _createItem(self, parent, name, className, icon):
        item = Qt.QTreeWidgetItem(parent, [name, className])
        item.setIcon(0, icon)
        #        item.setText(0, node.name)
        #        item.setText(1, class_.__name__)
        item.setExpanded(True)
        item.setFlags(item.flags() | Qt.Qt.ItemIsEditable);
        return item


@SingletonDecorator
class SceneManagerUI():
    def __init__(self):
        # UI
        self._mw = mw.MainWindow()
        self._smtw = SceneManagerTree()
        self._mw.createDockableWidget(self._smtw, "Scene Manager",
                                      dockAreaId=mw.DockAreaId.Left)

    @property
    def selectionChangedSignal(self):
        return self._smtw.ui.treeWidget.itemSelectionChanged

    @property
    def currentItemChangedSignal(self):
        return self._smtw.ui.treeWidget.currentItemChanged

    @property
    def selectedNodes(self):
        items = self._smtw.ui.treeWidget.selectedItems()
        if items is None:
            return None

        return [i.node for i in items if hasattr(i, 'node')]

    @selectedNodes.setter
    def selectedNodes(self, value):
        if not isinstance(value, Iterable):
            raise TypeError("Iterable expected.")

        if any(not isinstance(v, sc.SceneNode) for v in value):
            raise TypeError("value items must be SceneNodes.")

        self._smtw.ui.treeWidget.selectionModel().clear()

        for n in value:
            if n in self._nodes2Items:
                self._smtw.ui.treeWidget.setCurrentItem(
                    self._smtw._nodes2Items[n])

    @property
    def currentNode(self):
        item = self._smtw.ui.treeWidget.currentItem()

        if item is None:
            return None

        if hasattr(item, 'node'):
            return item.node

        return None

    @currentNode.setter
    def currentNode(self, value):
        if not isinstance(value, sc.SceneNode):
            raise TypeError("value must be a SceneNode.")

        if value in self._nodes2Items:
            self._smtw.ui.treeWidget.setCurrentItem(
                self._smtw._nodes2Items[value])


def init():
    SceneManagerUI()
#
#
#
# if __name__ == '__main__':
#    SMC = SceneManagerTree()
#    SMC.show()
