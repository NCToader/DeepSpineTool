# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:04:10 2019

@author: Marcos
#!todo: Gestion de cerrar modulo
"""

from app.core.utils import SingletonDecorator
from app.core import ui as mw
from app.plugins.ui import sceneManagerUi as scm

from app.plugins.model.image import Image

from app.plugins.ui.image.viewer.imShow3Widget import ImShow3Widget


# from app.plugins.ui.qbasics import CollapsableWidget
# from app.plugins.ui.image.viewer.mplFigureWidget import MplFigureWidget
# from app.plugins.ui.image.viewer._img3Renderer import BasicImg3Render
# from app.plugins.ui.image.viewer._img3Toolbar import Img3Toolbar


# recomendación que no derive de ImgShow3Widet. Esto premitiria ocultar alguno
# atributos públicos.
class Img3Viewer(ImShow3Widget):
    def __init__(self, imageNode, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(imageNode, Image):
            raise TypeError("Image node expected")

        self._imageNode = imageNode
        self.titleLabel.setStyleSheet("font: bold 20pt")
        self.titleLabel.setText(imageNode.name)

        self.img = imageNode.img
        self.renderer._createNewPlot()

        type(imageNode).img.connect2Attrib(self._imgChangedCB)
        type(imageNode).name.connect2Attrib(self._nameChangedCB)

    def _imgChangedCB(self, *args, **kwargs):
        self.img = self._imageNode.img
        print(self._imageNode.name, ' img changed' )

    def _nameChangedCB(self, *args, **kwargs):
        self.titleLabel.setText(self._imageNode.name)


@SingletonDecorator
class Img3ViewerManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Image", "Viewers"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "__##5426"
        self._name = "Basic Image 3D Viewer"

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
            i3v = Img3Viewer(imageNode)

            # !todo: No se pone el titulo porque habría que habilitar mecanismos
            #       para cerrar el widget y cambiar el titulo, si el nodo lo hace
            #            title = "Image 3D Viewer: " + imageNode.name
            self._mw.createDockableWidget(i3v, "Image 3D Viewer",
                                          dockAreaId=mw.DockAreaId.Right,
                                          hideOnClose=False)


def init(menuPath=None):
    Img3ViewerManager(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys
    import numpy as np
    from PyQt5 import Qt

    app = Qt.QApplication(sys.argv)

    image = Image(name='Test')
    img = np.zeros((6, 6, 6, 3), dtype='uint8')
    img[2:5, 2:5, 2:5, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    image.img = img




    #
    # image.img = img
    ex = Img3Viewer(image, figsize=(5, 3))
    img[2:5, 2:5, 2:5, :] = 255 * np.ones((3, 3, 3))
    ex.img= img
    #        ex.showToolbar= False
    #        ex.showToolbar = True
    #        ex.toolbarPosition = MplFigureWidget.ToolbarPosition.Left
    #        ex.showCoordinates=True
    #        ex.titlePosition = MplFigureWidget.ToolbarPosition.Bottom
    #        ex.figureCanvasMininumSize = (300,300)
    #        ex.figureHorizontalScrollBarPolicy = Qt.Qt.ScrollBarAlwaysOff
    #        ex.figureVerticalScrollBarPolicy = Qt.Qt.ScrollBarAlwaysOff
    #        ex.figureCanvasResizable = False
    #        ex.showToolbarCollapseButton = False
    #        ex.showTitleCollapseButton = False
    #        ex.showTitle = False

    ex.show()
    sys.exit(app.exec())
