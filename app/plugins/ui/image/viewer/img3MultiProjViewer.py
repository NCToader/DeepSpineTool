# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:27:29 2019

@author: Marcos García

#!todo: Botones pare el manejo en la ventana libre
#!todo: De forma general que no se cree un toolbar si no se va a utilizar!
"""

from PyQt5 import Qt

from app.plugins.model.image import Image

from app.core.utils import SingletonDecorator
from app.core import ui as mw
from app.plugins.ui import sceneManagerUi as scm

from app.plugins.ui.image.viewer.img3MultiProjWidget import Img3MultiProjWidget


class Img3MultiProjViewer(Img3MultiProjWidget):
    @staticmethod
    def uiInit(parent, ui):
        # Main Widgets
        #############################################
        parent.setObjectName("img3MultiProjViewer_form")

    def __init__(self, imageNode=None, parent=None, *args, **kwargs):
        super().__init__(img=None,  # if imageNode is None else imageNode.img, 
                         title=None,  # if imageNode is None else imageNode.name, 
                         parent=parent)

        self.uiInit(self, self._ui)

        self._imageNode = None
        self._setImageNode(imageNode)

    def _setImageNode(self, imageNode):
        if not (isinstance(imageNode, Image) or imageNode is None):
            raise TypeError("Image node expected")

        if self._imageNode is not None:
            type(imageNode).img.disconnectFromAttrib(self._imgChangedCB)
            type(imageNode).name.disconnectFromAttrib(self._nameChangedCB)
            self.img = None
            self.title = None
            self._imageNode = None

        if imageNode is not None:
            self._imageNode = imageNode
            self.img = imageNode.img
            self.title = imageNode.name
            type(imageNode).img.connect2Attrib(self._imgChangedCB)
            type(imageNode).name.connect2Attrib(self._nameChangedCB)

    #    @property
    #    def img(self):
    #        return super().img
    #         
    #    @property
    #    def title(self):
    #        return super().title

    @property
    def imageNode(self):
        return self._imageNode

    @imageNode.setter
    def imageNode(self, value):
        self._setImageNode(value)

    def _imgChangedCB(self, **kwargs):
        self.img = self._imageNode.img

    #        self._setImg (self._imageNode.img)

    def _nameChangedCB(self, **kwargs):
        self.title = self._imageNode.name


#        self._setTitle (self._imageNode.name)

@SingletonDecorator
class Img3MultiProjViewerManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Image", "Viewers"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%__%%2"
        self._name = "Image 3D Multiprojection Viewer"

        self._mw.addAction(self._name, prefix=self._prefix)
        self._mw.addActionCB(self._name,
                             self.addViewer,
                             prefix=self._prefix)
        self._mw.addAction2Menu(self._name,
                                menuPath=self._menuPath,
                                prefix=self._prefix)

    def addViewer(self):
        nodes = [n for n in self._smUI.selectedNodes \
                 if isinstance(n, Image) and \
                 n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")

        for imageNode in nodes:
            i3mpv = Img3MultiProjViewer(imageNode)
            i3mpv.createMaximumProjectionCheckBox(i3mpv.windowPanel)
            i3mpv.windowPanel.setSizePolicy(Qt.QSizePolicy.Expanding,
                                            Qt.QSizePolicy.Expanding)

            # !todo: No se pone el titulo porque habría que habilitar mecanismos
            #       para cerrar el widget y cambiar el titulo, si el nodo lo hace
            #            title = "Image 3D Viewer: " + imageNode.name
            self._mw.createDockableWidget(i3mpv,
                                          "Image 3D Multiprojection Viewer",
                                          dockAreaId=mw.DockAreaId.Right,
                                          hideOnClose=False)


def init(menuPath=None):
    Img3MultiProjViewerManager(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys
    import numpy as np
    import time

    app = Qt.QApplication(sys.argv)

    image = Image(name='Test')
    img = np.zeros((3, 6, 10, 3), dtype='int')
    img[:, 2:5, 4:7, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    image.img = img

    ex = Img3MultiProjViewer(image)
    ex.createMaximumProjectionCheckBox(ex.windowPanel)
    #        ex.windowPanel.setSizePolicy(Qt.QSizePolicy.Expanding,
    #                                     Qt.QSizePolicy.Expanding)

    ex.show()

    time.sleep(2)

    image.img[:, 2:5, 4:7, :] = 255 * np.ones((3, 3, 3, 3))
    type(image).img.touch(image);

    sys.exit(app.exec())
