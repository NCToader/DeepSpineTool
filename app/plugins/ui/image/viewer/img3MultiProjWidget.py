# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:27:29 2019

@author: URJC

#!todo: Botones pare el manejo en la ventana libre
#!todo: De forma general que no se cree un toolbar si no se va a utilizar!
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

from app.plugins.ui.qbasics.gridWidget import GridWidget
from app.plugins.ui.qbasics import CollapsableWidget
from app.plugins.ui.image.viewer.imShow3Widget import ImShow3Widget
from app.plugins.ui.image.viewer.mplFigureWidget import MplFigureWidget
from app.plugins.ui.image.viewer._img3Renderer import Img3RenderABC


class Img3MultiProjWidget(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("img3MultiProjWidget_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            self.title_form = CollapsableWidget(parent=parent,
                                                position=CollapsableWidget.Position.Top)
            self.title_widget = Qt.QWidget()
            self.title_label = Qt.QLabel(parent=self.title_widget)
            f = Qt.QFont("Arial", 20, Qt.QFont.Bold)
            self.title_label.setFont(f)
            self.title_label.setAlignment(Qt.Qt.AlignCenter)
            self.title_form.addWidget(self.title_widget)

            self.panel_widget = Qt.QWidget()
            self.grid_widget = GridWidget(parent=parent)
            self.projViewers = dict()
            self.projViewers['xy'] = ImShow3Widget(*args, **kwargs)
            self.projViewers['zy'] = ImShow3Widget(*args, **kwargs)
            self.projViewers['xz'] = ImShow3Widget(*args, **kwargs)
            self.grid_widget.addWidget(self.projViewers['xy'])
            self.grid_widget.addWidget(self.projViewers['zy'])
            self.grid_widget.addWidget(self.projViewers['xz'])
            self.grid_widget.addWidget(self.panel_widget)

            #            self.projViewers['xy'].showImgToolbarShowAllButton = False
            #            self.projViewers['xy'].showImgToolbarZoomToData = False
            #            self.projViewers['xy'].showImgToolbarProjectionPanel = False
            #            self.projViewers['z'].showImgToolbarShowAllButton = False
            #            self.projViewers['z'].showImgToolbarZoomToData = False
            #            self.projViewers['z'].showImgToolbarProjectionPanel = False
            #            self.projViewers['xz'].showImgToolbarShowAllButton = False
            #            self.projViewers['xz'].showImgToolbarZoomToData = False
            #            self.projViewers['xz'].showImgToolbarProjectionPanel = False
            self.projViewers['xy'].showImgToolbarButtonPanel = False
            self.projViewers['zy'].showImgToolbarButtonPanel = False
            self.projViewers['xz'].showImgToolbarButtonPanel = False

            self.projViewers['xy'].toolbarPosition = \
                MplFigureWidget.ToolbarPosition.Left
            self.projViewers['zy'].toolbarPosition = \
                MplFigureWidget.ToolbarPosition.Right
            self.projViewers['xz'].toolbarPosition = \
                MplFigureWidget.ToolbarPosition.Left

            f = Qt.QFont("Arial", 15, Qt.QFont.Bold)
            self.projViewers['xy'].titleLabel.setFont(f)
            self.projViewers['zy'].titleLabel.setFont(f)
            self.projViewers['xz'].titleLabel.setFont(f)

            self.projViewers['xy'].renderer.projectionPlane = \
                Img3RenderABC.ProjectionPlane.XY
            self.projViewers['zy'].renderer.projectionPlane = \
                Img3RenderABC.ProjectionPlane.ZY
            self.projViewers['xz'].renderer.projectionPlane = \
                Img3RenderABC.ProjectionPlane.XZ

            # Creación de los layouts
            #############################################
            #            self.layout = Qt.QGridLayout(parent = parent)
            self.layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                        parent=parent)

            self.layout.setSpacing(0)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setObjectName("main_layout")

            self.layout.addWidget(self.title_form)
            self.layout.addWidget(self.grid_widget)

            # No se almacena por sise quiere cambiar
            panel_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                         parent=self.panel_widget)
            panel_layout.setSpacing(0)
            panel_layout.setContentsMargins(0, 0, 0, 0)

            self.title_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                              parent=self.title_widget)
            self.title_layout.setSpacing(0)
            self.title_layout.setContentsMargins(0, 0, 0, 0)
            self.title_layout.addWidget(self.title_label)

    def __init__(self, img=None, title=None, parent=None,
                 *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = Img3MultiProjWidget._UI(self, *args, **kwargs)

        self._ui.projViewers['xy'].renderer.xlimChangedSignal.connect(
            self._xlimChanged)
        self._ui.projViewers['xz'].renderer.xlimChangedSignal.connect(
            self._xlimChanged)
        self._ui.projViewers['xy'].renderer.ylimChangedSignal.connect(
            self._ylimChanged)
        self._ui.projViewers['zy'].renderer.ylimChangedSignal.connect(
            self._ylimChanged)
        self._ui.projViewers['xz'].renderer.ylimChangedSignal.connect(
            self._zlimChanged)
        self._ui.projViewers['zy'].renderer.xlimChangedSignal.connect(
            self._zlimChanged)

        #        self._setImg (img)
        #        self._setTitle (title)
        self.img = img
        self.title = title

    #        type(imageNode).img.connect2Attrib(self._imgChangedCB)
    #        type(imageNode).name.connect2Attrib(self._nameChangedCB)

    @property
    def windowPanel(self):
        return self._ui.panel_widget

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._ui.projViewers['xy'].img = value
        self._ui.projViewers['zy'].img = value
        self._ui.projViewers['xz'].img = value
        self._ui.projViewers['xy'].renderer._createNewPlot()
        self._ui.projViewers['zy'].renderer._createNewPlot()
        self._ui.projViewers['xz'].renderer._createNewPlot()
        self._img = value

    #        self._setImg(value)

    #    def _setImg(self, value):
    #        el control de tipo se hace en el renderer
    #        self._ui.projViewers['xy'].img = value
    #        self._ui.projViewers['zy'].img = value
    #        self._ui.projViewers['xz'].img = value
    #        self._img = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not (isinstance(value, str) or value is None):
            raise TypeError("String value expected")

        self._title = "" if value is None else value
        self._ui.title_label.setText(self._title)
        self._ui.projViewers['xy'].titleLabel.setText("XY " + self._title)
        self._ui.projViewers['zy'].titleLabel.setText("ZY " + self._title)
        self._ui.projViewers['xz'].titleLabel.setText("XZ " + self._title)

    #        self._setTitle (value)

    #    def _setTitle(self, value):
    #        if not (isinstance (value, str) or value is None):
    #            raise TypeError("String value expected")
    #        
    #        self._title = "" if value is None else value
    #        self._ui.title_label.setText(self._title)
    #        self._ui.projViewers['xy'].titleLabel.setText("XY " + self._title)
    #        self._ui.projViewers['zy'].titleLabel.setText("ZY " + self._title)
    #        self._ui.projViewers['xz'].titleLabel.setText("XZ " + self._title)

    def createMaximumProjectionCheckBox(self, parent, *args, **kwargs):
        self._ui.maximumProj_checkbox = Qt.QCheckBox(parent)
        self._ui.maximumProj_checkbox.setText("Maximun projection")
        if parent.layout() is not None:
            parent.layout().addWidget(self._ui.maximumProj_checkbox,
                                      *args, **kwargs)
        self._ui.maximumProj_checkbox.clicked.connect(self._mpCheckboxClicked)

    @Qt.pyqtSlot(int, int)
    def _xlimChanged(self, mn, mx):
        self._ui.projViewers['xy'].renderer.xlim = (mn, mx)
        self._ui.projViewers['xz'].renderer.xlim = (mn, mx)

    @Qt.pyqtSlot(int, int)
    def _ylimChanged(self, mn, mx):
        self._ui.projViewers['zy'].renderer.ylim = (mn, mx)
        self._ui.projViewers['xy'].renderer.ylim = (mn, mx)

    @Qt.pyqtSlot(int, int)
    def _zlimChanged(self, mn, mx):
        self._ui.projViewers['zy'].renderer.xlim = (mn, mx)
        self._ui.projViewers['xz'].renderer.ylim = (mn, mx)

    @Qt.pyqtSlot(bool)
    def _mpCheckboxClicked(self, checked):
        self._ui.projViewers['xy'].renderer.showMaximumProjection = checked
        self._ui.projViewers['zy'].renderer.showMaximumProjection = checked
        self._ui.projViewers['xz'].renderer.showMaximumProjection = checked


if __name__ == '__main__':
    #    try:
    import sys
    import numpy as np

    app = Qt.QApplication(sys.argv)

    img = np.zeros((3, 6, 10, 3), dtype='int')
    img[:, 2:5, 4:7, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)

    ex = Img3MultiProjWidget(img=img)
    ex.createMaximumProjectionCheckBox(ex.windowPanel)
    #        ex.windowPanel.setSizePolicy(Qt.QSizePolicy.Expanding,
    #                                     Qt.QSizePolicy.Expanding)

    ex.show()
    ex.img = 0.5 * np.ones((3, 3, 3, 3))

    sys.exit(app.exec())
