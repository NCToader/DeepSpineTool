# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:29:14 2019

@author: URJC
"""

from PyQt5 import Qt

from app.core.utils import SingletonDecorator
from app.core.model import Scene, SceneNode
from app.plugins.model.meshNode.meshNode import MeshNode

from app.plugins.model.folder import Folder
from app.plugins.model.image import Image, Image2, Image3

import app.plugins.ui.iconManager.iconResources


@SingletonDecorator
class NodeIconManager:
    def __init__(self):
        self._node2Icon = dict()
        self.setNodeIcon(SceneNode, Qt.QIcon(":/Nodes/Icons/node"))
        self.setNodeIcon(Scene(), Qt.QIcon(":/Nodes/Icons/tree"))
        self.setNodeIcon(Folder, Qt.QIcon(":/Nodes/Icons/Folder"))
        self.setNodeIcon(Image, Qt.QIcon(":/Nodes/Icons/image"))
        self.setNodeIcon(Image2, Qt.QIcon(":/Nodes/Icons/image2"))
        self.setNodeIcon(Image3, Qt.QIcon(":/Nodes/Icons/image3"))
        self.setNodeIcon(MeshNode, Qt.QIcon(":/Nodes/Icons/meshNode"))

    #        print ("Existe: ", Qt.QFile(":/Icons/Icons/node.jpg").exists())
    #        file = Qt.QFile(":/Icons/Icons/node.jpg")
    #        file.open(Qt.QIODevice.ReadOnly) 
    #        print (file.readAll());
    #        file.close();
    #        icon = Qt.QImage()
    #        print ("Carga: ", icon.load(":/Icons/Icons/node.jpg"))
    #        print(icon.size().height(),icon.size().width()) 

    # =============================================================================
    #   Gestión de iconos      
    # =============================================================================

    def setNodeIcon(self, class_, icon):
        name = class_.getClassName()
        #        if self._node2Icon.get(name) is None:
        if not isinstance(icon, Qt.QIcon):
            raise ValueError("Error: The second parameter must be a QIcon")
        self._node2Icon[name] = icon

    def getNodeIcon(self, class_):
        classNames = class_.getClassNameHierarchy()

        for c in classNames:
            if c in self._node2Icon:
                return self._node2Icon[c]
