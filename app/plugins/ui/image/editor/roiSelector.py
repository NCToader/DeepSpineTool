# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:27:16 2019

@author: URJC

#!todo: Oculta el RectangleSelector, dependiendo del valor del slider. Tener
#       en cuent MP. 
#!todo: Rehacer las cajas si cambia la imagen 
#!todo: meter la transformación respecto de la imagen padre.
#!todo: Definir un tamaño mínimo de Roy
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
from matplotlib.widgets import RectangleSelector
import numpy as np

from app.plugins.model.image import Image

from app.core.utils import SingletonDecorator
from app.core import ui as mw
from app.core import model as sc
from app.plugins.ui import sceneManagerUi as scm

from app.plugins.ui.image.viewer.img3MultiProjViewer import Img3MultiProjViewer


# from app.plugins.ui.qbasics.gridWidget import GridWidget
# from app.plugins.ui.qbasics import CollapsableWidget
# from app.plugins.ui.image.viewer.imShow3Widget import ImShow3Widget
# from app.plugins.ui.image.viewer.mplFigureWidget import MplFigureWidget
# from app.plugins.ui.image.viewer._img3Renderer import Img3RenderABC


class ROISelector(Img3MultiProjViewer):
    class _Box:
        def __init__(self):
            self._box = [0, 0, 0, 0, 0, 0]

        def allNull(self):
            return (self._box[0] - self._box[1]) == 0 and \
                   (self._box[2] - self._box[3]) == 0 and \
                   (self._box[4] - self._box[5]) == 0

        def anyNull(self):
            return (self._box[0] - self._box[1]) == 0 or \
                   (self._box[2] - self._box[3]) == 0 or \
                   (self._box[4] - self._box[5]) == 0

        @property
        def box(self): return tuple(self._box)

        @box.setter
        def box(self, value): self._box = list(value)

        @property
        def x(self): return tuple(self._box[0:2])

        @x.setter
        def x(self, value): self._box[0:2] = list(value)

        @property
        def y(self): return tuple(self._box[2:4])

        @y.setter
        def y(self, value): self._box[2:4] = list(value)

        @property
        def z(self): return tuple(self._box[4:6])

        @z.setter
        def z(self, value): self._box[4:6] = list(value)

    def __init__(self, imageNode, *args, parent=None, **kwargs):
        super().__init__(imageNode, *args, parent=parent, **kwargs)

        # =============================================================================
        #       Rectangle Selector
        # =============================================================================
        self._box = ROISelector._Box()

        kwargs = {'drawtype': 'box', 'useblit': False, 'button': [1],
                  'minspanx': 5, 'minspany': 5,
                  'spancoords': 'pixels', 'interactive': True}
        self._rs = dict()
        self._rs['xy'] = RectangleSelector(
            self._ui.projViewers['xy'].renderer.ax,
            lambda x, y: self._setBox('xy'), **kwargs)

        self._rs['zy'] = RectangleSelector(
            self._ui.projViewers['zy'].renderer.ax,
            lambda x, y: self._setBox('zy'), **kwargs)

        self._rs['xz'] = RectangleSelector(
            self._ui.projViewers['xz'].renderer.ax,
            lambda x, y: self._setBox('xz'), **kwargs)

        self._setRS()

        # !Todo: Ver si se puede activar el useblit (Más rápido)
        #       No se por que no va
        #        def p():
        #                if self._rs['xy'].active:
        #                    self._rs['xy'].update()
        #        self._ui.projViewers['xy'].renderer.postdrawSignal.connect(p)

        # =============================================================================
        #       Botonera
        # =============================================================================
        panel = self.windowPanel
        self._ui.buttons_widget = Qt.QWidget(panel)
        if panel.layout() is not None:
            panel.layout().addWidget(self._ui.buttons_widget)

        self._ui.buttons_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                                parent=self._ui.buttons_widget)
        self._ui.buttons_layout.setSpacing(2)
        self._ui.buttons_layout.setContentsMargins(0, 0, 0, 0)

        self._ui.createButton = Qt.QPushButton('Create ROI')
        self._ui.buttons_layout.addWidget(self._ui.createButton)
        self.createMaximumProjectionCheckBox(self._ui.buttons_widget)

        # =============================================================================
        #       Callbacks
        # =============================================================================
        self._ui.createButton.clicked.connect(self._createROI)

    @Qt.pyqtSlot()
    def _createROI(self):
        if self._box.anyNull():
            mw.MainWindow().warningMsg("Please select a 3D box")
            return

        img = self._imageNode.img

        box = np.array(self._box.box)
        for i in range(3):
            if box[2 * i] > box[2 * i + 1]:
                b = box[2 * i]
                box[2 * i] = box[2 * i + 1]
                box[2 * i + 1] = b

        box[[0, 2, 4]] = np.maximum(np.floor(box[[0, 2, 4]]), 0)
        box[[1, 3, 5]] = np.minimum(np.ceil(box[[1, 3, 5]]) + 1, img.shape[2::-1])
        box = box.astype(int)
        x0, x1, y0, y1, z0, z1 = tuple(box)

        node = Image(name='ROI')
        if len(img.shape) == 4:
            node.img = img[z0:z1, y0:y1, x0:x1, :]
        else:
            node.img = img[z0:z1, y0:y1, x0:x1]
            node.nDims = Image.Dims.img3D

        sc.Scene().addNode2Parent(node=node, parent=self._imageNode)

    def _setRS(self):
        self._rs['xy'].extents = tuple((*self._box.x, *self._box.y))
        self._rs['zy'].extents = tuple((*self._box.z, *self._box.y))
        self._rs['xz'].extents = tuple((*self._box.x, *self._box.z))

        if self._box.allNull():
            for k in self._rs:
                self._rs[k].set_visible(False)
        else:
            for k in self._rs:
                self._rs[k].set_visible(True)

    def _setBox(self, id_):
        x1, x2, y1, y2 = self._rs[id_].extents

        if id_ == 'xy':
            self._box.x = (x1, x2)
            self._box.y = (y1, y2)
        elif id_ == 'zy':
            self._box.z = (x1, x2)
            self._box.y = (y1, y2)
        elif id_ == 'xz':
            self._box.x = (x1, x2)
            self._box.z = (y1, y2)

        self._setRS()


@SingletonDecorator
class ROISelectorManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Image", "Editors"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$%$2"
        self._name = "ROI Selector"

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
            rs = ROISelector(imageNode)

            # !todo: No se pone el titulo porque habría que habilitar mecanismos
            #       para cerrar el widget y cambiar el titulo, si el nodo lo hace
            #            title = "Image 3D Viewer: " + imageNode.name
            self._mw.createDockableWidget(rs,
                                          "ROI Selector",
                                          dockAreaId=mw.DockAreaId.Right,
                                          hideOnClose=False)


def init(menuPath=None):
    ROISelectorManager(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys

    app = Qt.QApplication(sys.argv)

    image = Image(name='Test')
    img = np.zeros((3, 6, 10, 3), dtype='uint8')
    img[:, 2:5, 4:7, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    image.img = img

    ex = ROISelector(image)

    img[:, 2:5, 4:7, :] = 255 * np.ones((3, 3, 3))

    image.img = img

    ex.show()
    sys.exit(app.exec())
