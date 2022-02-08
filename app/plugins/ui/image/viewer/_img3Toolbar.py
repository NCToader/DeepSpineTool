# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:20:15 2019

@author: Marcos García
#!todo: Podría Reducir los Enums. 



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
from enum import Enum

from app.plugins.ui.image.viewer._img3Renderer import Img3RenderABC

from app.plugins.ui.image.viewer.ui_Image3Toolbar import \
    Ui_image3Toolbar_widget


class Img3Toolbar(Qt.QWidget):
    class Orientation(Enum):
        Horizontal = True
        Vertical = False

    def __init__(self, renderer, parent=None):
        if not isinstance(renderer, Img3RenderABC):
            raise TypeError("_Img3RenderABC expected")

        # Interface Setup
        super().__init__(parent)
        self._ui = Ui_image3Toolbar_widget()
        self._ui.setupUi(self)
        self._ui.horizontalZ_label.setText("0")
        self._ui.verticalZ_label.setText("0")

        # adding render
        self._renderer = renderer
        self._renderer.rangeUpdatedSignal.connect(self._setRange)
        self._renderer.sliceUpdatedSignal.connect(self._setSliceIdx)
        self._renderer.showMaximumProjectionSignal.connect(self._setMP)
        self._renderer.projectionPlaneSignal.connect(self._setProjPlane)

        # interface intit
        self._orientation = Img3Toolbar.Orientation.Horizontal
        self._setOrientation()

        self._projPlaneToButton = dict()
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.XY] = \
            self._ui.horizontalPlaneXY_toolButton
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.YX] = \
            self._ui.horizontalPlaneXY_toolButton
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.YZ] = \
            self._ui.horizontalPlaneYZ_toolButton
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.ZY] = \
            self._ui.horizontalPlaneYZ_toolButton
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.ZX] = \
            self._ui.horizontalPlaneZX_toolButton
        self._projPlaneToButton[Img3RenderABC.ProjectionPlane.XZ] = \
            self._ui.horizontalPlaneZX_toolButton

        self._buttonToProjPlane = dict()
        # !todo:Poder seleccionar entre Img3RenderABC.ProjectionPlane.XY e YX...
        self._buttonToProjPlane[self._ui.horizontalPlaneXY_toolButton] = \
            Img3RenderABC.ProjectionPlane.XY
        self._buttonToProjPlane[self._ui.horizontalPlaneYZ_toolButton] = \
            Img3RenderABC.ProjectionPlane.ZY
        self._buttonToProjPlane[self._ui.horizontalPlaneZX_toolButton] = \
            Img3RenderABC.ProjectionPlane.XZ

        self._setRange()
        #        self._setSliceIdx() #Not needed _setRange
        self._setMP()
        self._setProjPlane()

        self._ui.horizontalZ_slider.valueChanged.connect(self._sliderMoved)

        self._ui.horizontalShowAll_pushButton.clicked.connect(
            self._showAllButtonClicked)
        self._ui.verticalShowAll_pushButton.clicked.connect(
            self._showAllButtonClicked)

        self._ui.horizontalZoomToData_pushButton.clicked.connect(
            self._zoomToDataButtonClicked)
        self._ui.verticalZoomToData_pushButton.clicked.connect(
            self._zoomToDataButtonClicked)

        #        self._ui.horizontalMP_checkBox.stateChanged(int 0 2) #mejor clicked solo eventos del interfaz
        self._ui.horizontalMP_checkBox.clicked.connect(self._mpCheckboxClicked)
        self._ui.verticalMP_checkBox.clicked.connect(self._mpCheckboxClicked)

        self._ui.horizontalPlaneXY_toolButton.toggled.connect(
            self._projPlaneButtonClicked)
        self._ui.horizontalPlaneYZ_toolButton.toggled.connect(
            self._projPlaneButtonClicked)
        self._ui.horizontalPlaneZX_toolButton.toggled.connect(
            self._projPlaneButtonClicked)

    def _setOrientation(self):
        horizontal = self._orientation.value
        self._ui.horizontal_widget.setVisible(horizontal)
        self._ui.vertical_widget.setVisible(not horizontal)

    @Qt.pyqtSlot()
    def _setRange(self):
        smin, smax = self._renderer.depthRange

        self._ui.horizontalZ_slider.setMaximum(smax)
        self._ui.horizontalZ_slider.setMinimum(smin)

        self._ui.horizontalZ_slider.setSliderPosition(self._renderer.sliceIdx)

    @Qt.pyqtSlot()
    def _setSliceIdx(self):
        self._ui.horizontalZ_slider.setSliderPosition(self._renderer.sliceIdx)

    @Qt.pyqtSlot()
    def _setMP(self):
        self._ui.horizontalMP_checkBox.setCheckState(
            Qt.Qt.Checked if self._renderer.showMaximumProjection \
                else Qt.Qt.Unchecked)

    @Qt.pyqtSlot()
    def _setProjPlane(self):
        self._projPlaneToButton[self._renderer.projectionPlane].setChecked(True)

    @Qt.pyqtSlot(int)
    def _sliderMoved(self, slc):
        self._renderer.sliceIdx = slc

    @Qt.pyqtSlot()
    def _showAllButtonClicked(self):
        self._renderer.showAll()

    @Qt.pyqtSlot()
    def _zoomToDataButtonClicked(self):
        self._renderer.zoomToData()

    @Qt.pyqtSlot(bool)
    def _mpCheckboxClicked(self, checked):
        self._renderer.showMaximumProjection = checked

    @Qt.pyqtSlot(bool)
    def _projPlaneButtonClicked(self, checked):
        if checked:
            self._renderer.projectionPlane = \
                self._buttonToProjPlane[self.sender()]

    #    @property
    #    def depthRange(self):
    #        return self._renderer.depthRange
    #    
    #    @property
    #    def sliceIdx(self):
    #        return self._renderer._sliceIdx
    #    
    #    @depthRange.setter
    #    def depthRange(self, value):
    #        if not isinstance (value, tuple):
    #            raise TypeError("Tuple expected")   
    #        
    #        if len(value) != 2:
    #            raise AttributeError ("2 components expecte")
    #        elif not np.issubdtype(np.array(value).dtype, np.integer):
    #            raise AttributeError ("Integers expected")
    ##        elif value[0]<0 or value[1]<0:
    ##            raise AttributeError("Positive values expected")
    #        elif value[0]>value[1]:
    #            raise AttributeError("Invalide value: "+ str(value))
    #            
    #        self._renderer.depthRange = value
    #        self._setRange()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if not isinstance(value, Img3Toolbar.Orientation):
            raise TypeError("Image3Toolbar.Orientation expected")

        self._orientation = value
        self._setOrientation()

    @property
    def showShowAllButton(self):
        return not (self._ui.verticalShowAll_pushButton.isHidden() and \
                    self._ui.horizontalShowAll_pushButton.isHidden())

    @showShowAllButton.setter
    def showShowAllButton(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._ui.verticalShowAll_pushButton.setVisible(value)
        self._ui.horizontalShowAll_pushButton.setVisible(value)

    @property
    def showZoomToData(self):
        return not (self._ui.verticalZoomToData_pushButton.isHidden() and \
                    self._ui.horizontalZoomToData_pushButton.isHidden())

    @showZoomToData.setter
    def showZoomToData(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._ui.verticalZoomToData_pushButton.setVisible(value)
        self._ui.horizontalZoomToData_pushButton.setVisible(value)

    @property
    def showMaximumProjection(self):
        return not (self._ui.horizontalMP_widget.isHidden() and \
                    self._ui.verticalMP_widget.isHidden())

    @showMaximumProjection.setter
    def showMaximumProjection(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._ui.verticalMP_widget.setVisible(value)
        self._ui.horizontalMP_widget.setVisible(value)

    @property
    def showProjectionPanel(self):
        return not (self._ui.verticalPlaneSelector_widget.isHidden() and \
                    self._ui.horizontalPlaneSelector_widget.isHidden())

    @showProjectionPanel.setter
    def showProjectionPanel(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._ui.verticalPlaneSelector_widget.setVisible(value)
        self._ui.horizontalPlaneSelector_widget.setVisible(value)

    @property
    def showButtonPanel(self):
        return not (self._ui.verticalButtons_widget.isHidden() and \
                    self._ui.horizontalButtons_widget.isHidden())

    @showButtonPanel.setter
    def showButtonPanel(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._ui.verticalButtons_widget.setVisible(value)
        self._ui.horizontalButtons_widget.setVisible(value)

    @property
    def showSliderPanel(self):
        return not (self._ui.verticalSlider_widget.isHidden() and \
                    self._ui.verticalSlider_widget.isHidden())

    @showSliderPanel.setter
    def showSliderPanel(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._ui.verticalSlider_widget.setVisible(value)
        self._ui.verticalSlider_widget.setVisible(value)


if __name__ == '__main__':
    import sys
    import numpy as np
    from app.plugins.ui.image.viewer._img3Renderer import BasicImg3Render
    from app.plugins.ui.image.viewer.mplFigureWidget import MplFigureWidget

    app = Qt.QApplication(sys.argv)

    mpl = MplFigureWidget(figsize=(5, 3))
    mpl.show()
    bir = BasicImg3Render(mpl.figure)

    tlb = Img3Toolbar(bir)
    tlb.show()

    img = np.zeros((6, 6, 6, 3), dtype='int')
    img[2:5, 2:5, 2:5, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    bir.img = img

    print(bir.depthRange)
    print(bir.sliceIdx)

    #    print(ex.orientation)
    #    print(ex.showShowAllButton)
    #    print(ex.showZoomToData)
    #    print(ex.showMaximumProjection)
    #    print(ex.showProjectionPanel)
    #    print(ex.showButtonPanel)
    #    print(ex.showSliderPanel)
    #    print(ex.depthRange)

    tlb.orientation = Img3Toolbar.Orientation.Vertical
    #    bi.title = "Hola"        
    #    bi.sliceIdx = 3
    #    bi.projectionPlane = Img3RenderABC.ProjectionPlane.XY
    #    bi.showMaximumProjection = True
    #    bi.zoomToData()
    #    bi.showAll()

    #    ex.showShowAllButton         = False
    #    ex.showZoomToData            = False
    #    ex.showMaximumProjection     = False
    #    ex.showProjectionPanel       = False
    #    ex.showButtonPanel           = False
    #    ex.showSliderPanel           = False

    sys.exit(app.exec())
