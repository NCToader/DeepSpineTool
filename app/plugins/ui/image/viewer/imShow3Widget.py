# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:54:58 2019

@author: URJC

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

from app.plugins.ui.qbasics import CollapsableWidget
from app.plugins.ui.image.viewer.mplFigureWidget import MplFigureWidget
from app.plugins.ui.image.viewer._img3Renderer import BasicImg3Render
from app.plugins.ui.image.viewer._img3Toolbar import Img3Toolbar


class ImShow3Widget(MplFigureWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bir = BasicImg3Render(self.figure)

        # Se crea y se añade el toolbar

        self._ui.imgToolbar_form = CollapsableWidget(self,
                                                     position=CollapsableWidget.Position.Bottom)
        self._ui.i3tlb = Img3Toolbar(self._bir,
                                     parent=self._ui.imgToolbar_form)
        self._ui.imgToolbar_form.addWidget(self._ui.i3tlb)
        self._ui.panel_widget = Qt.QWidget()

        # !todo:meter metodos que te dejen modificar el layout central????
        self._ui.central_layout.addWidget(self._ui.imgToolbar_form)
        self._ui.central_layout.addWidget(self._ui.panel_widget)

        panel_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                     parent=self._ui.panel_widget)
        panel_layout.setSpacing(0)
        panel_layout.setContentsMargins(0, 0, 0, 0)

    @property
    def windowPanel(self):
        return self._ui.panel_widget

    @property
    def renderer(self):
        return self._bir

    @property
    def imgToolbar(self):
        return self._ui.i3tlb

    @property
    def img(self):
        return self._bir.img

    @img.setter
    def img(self, value):
        self._bir.img = value
        self._bir.touch()

    @property
    def showImgToolbar(self):
        return self._ui.imgToolbar_form.isVisible()

    @showImgToolbar.setter
    def showImgToolbar(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        if value:
            self._ui.imgToolbar_form.show()
        else:
            self._ui.imgToolbar_form.hide()

    # !Todo: Podrían quitarse ya que hay acceso al Toolbar
    # !Todo: dar acceso en la clase padre al toolbar de navegación.?
    @property
    def showImgToolbarCollapseButton(self):
        return self._ui.i3tlb.showCollapseButton

    @showImgToolbarCollapseButton.setter
    def showImgToolbarCollapseButton(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._ui.i3tlb.showCollapseButton = value

    @property
    def showImgToolbarShowAllButton(self):
        return self._ui.i3tlb.showShowAllButton

    @showImgToolbarShowAllButton.setter
    def showImgToolbarShowAllButton(self, value):
        self._ui.tlb.showShowAllButton = value

    @property
    def showImgToolbarZoomToData(self):
        return self._ui.i3tlb.showZoomToData

    @showImgToolbarZoomToData.setter
    def showImgToolbarZoomToData(self, value):
        self._ui.tlb.showZoomToData = value

    @property
    def showImgToolbarMaximumProjection(self):
        return self._ui.i3tlb.showMaximumProjection

    @showImgToolbarMaximumProjection.setter
    def showImgToolbarMaximumProjection(self, value):
        self._ui.tlb.showMaximumProjection = value

    @property
    def showImgToolbarProjectionPanel(self):
        return self._ui.i3tlb.showProjectionPanel

    @showImgToolbarProjectionPanel.setter
    def showImgToolbarProjectionPanel(self, value):
        self._ui.i3tlb.showProjectionPanel = value

    @property
    def showImgToolbarButtonPanel(self):
        return self._ui.i3tlb.showButtonPanel

    @showImgToolbarButtonPanel.setter
    def showImgToolbarButtonPanel(self, value):
        self._ui.i3tlb.showButtonPanel = value

    @property
    def showImgToolbarSliderPanel(self):
        return self._ui.i3tlb.showSliderPanel

    @showImgToolbarSliderPanel.setter
    def showImgToolbarSliderPanel(self, value):
        self._ui.i3tlb.showSliderPanel = value

    def _setToolbarPosition(self):
        super()._setToolbarPosition()
        # todo: La primera vez que se llama estos objetos no están creados.
        #       poner más elegante

        if hasattr(self._ui, "imgToolbar_form"):
            v = self._toolbarPosition
            self._ui.imgToolbar_form.position = v.value

            if MplFigureWidget.ToolbarPosition.Top == v or \
                    MplFigureWidget.ToolbarPosition.Bottom == v:
                self._ui.i3tlb.orientation = \
                    Img3Toolbar.Orientation.Horizontal
            else:
                self._ui.i3tlb.orientation = \
                    Img3Toolbar.Orientation.Vertical


if __name__ == '__main__':
    #    try:
    from PyQt5 import Qt
    import sys
    import numpy as np

    app = Qt.QApplication(sys.argv)

    img = np.zeros((6, 6, 6, 3), dtype='int')
    img[2:5, 2:5, 2:5, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)

    ex = ImShow3Widget()
    ex.img = img

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
