# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:23:55 2019

@author: Marcos García

plt.subplots(2, 2) Crea figura y ejes. ptl.legend, ptl.show
 
Figura todo, Axes subregion. Axis eje, Artist (text, line...),  GridSpec
 
Axes -> set_xlim(), set_title, ylabel

https://matplotlib.org/tutorials/index.html
"""

#########################################3
# ver
# https://stackoverflow.com/questions/15582105/python-plot-stacked-image-slices
##############################################################################

import numpy as np
import matplotlib.pyplot as plt
import numbers as num

from abc import abstractmethod, ABC  # , abstractproperty
from enum import Enum
from PyQt5 import Qt

from app.plugins.utils.image.image import getAABBImg, rgb2grayStack
from app.plugins.utils.image.colorMapUtils import createColorMap


class _Img3RenderMeta(type(Qt.QObject), type(ABC)):
    pass


class Img3RenderABC(Qt.QObject, ABC, metaclass=_Img3RenderMeta):
    class ProjectionPlane(Enum):
        XY = (0, False)
        YX = (0, True)
        ZY = (2, True)
        YZ = (2, False)
        XZ = (1, False)
        ZX = (1, True)

    # dataSignals
    dataUpdatedSignal = Qt.pyqtSignal()
    rangeUpdatedSignal = Qt.pyqtSignal(int, int)
    sliceUpdatedSignal = Qt.pyqtSignal(int)

    # Visualization signals
    showAllSignal = Qt.pyqtSignal()
    zoomToDataSignal = Qt.pyqtSignal()
    projectionPlaneSignal = Qt.pyqtSignal(ProjectionPlane)
    showMaximumProjectionSignal = Qt.pyqtSignal(bool)
    titleUpdatedSignal = Qt.pyqtSignal(str)

    predrawSignal = Qt.pyqtSignal()
    postdrawSignal = Qt.pyqtSignal()

    @abstractmethod
    def __init__(self, figure, parent=None):
        Qt.QObject.__init__(self, parent)
        self._fig = figure
        self._title = None

        self._projPlane = Img3RenderABC.ProjectionPlane.XY
        self._showMP = False

        self._range = (0, 0)
        self._slice = 0

        # si llamas a auna función que renderice se mete en un bucle

    #       self._fig.canvas.mpl_connect('draw_event', self._emitDrawSignal)

    def showAll(self):
        self._showAll()
        self.showAllSignal.emit()

    def zoomToData(self):
        self._zoomToData()
        self.zoomToDataSignal.emit()

    @property
    def projectionPlane(self):
        return self._projPlane

    @projectionPlane.setter
    def projectionPlane(self, value):
        if not isinstance(value, Img3RenderABC.ProjectionPlane):
            raise TypeError("Img3RenderABC.ProjectionPlane expected")

        if self._projPlane != value:
            self._projPlane = value
            self._setProjetionPlane()
            self.projectionPlaneSignal.emit(self._projPlane)

    @property
    def showMaximumProjection(self):
        return self._showMP

    @showMaximumProjection.setter
    def showMaximumProjection(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        if self._showMP != value:
            self._showMP = value
            self._setMaximumProjection()
            self.showMaximumProjectionSignal.emit(self._showMP)

    @property
    def sliceIdx(self):
        return self._slice

    @sliceIdx.setter
    def sliceIdx(self, value):
        if not isinstance(value, int):
            raise TypeError("Int expected")
        elif self._range[0] > value or self._range[1] < value:
            raise TypeError("value out of range")

        if self._slice != value:
            self._slice = value
            self._setSlice()
            self.sliceUpdatedSignal.emit(self._slice)

    @property
    def depthRange(self):
        return self._range

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("String expected")

        self._title = value
        self._fig.suptitle(value)
        self.titleUpdatedSignal.emit(value)

    @abstractmethod
    def _setMaximumProjection(self):
        pass

    @abstractmethod
    def _setProjetionPlane(self):
        pass

    @abstractmethod
    def _setSlice(self):
        pass

    @abstractmethod
    def _zoomToData(self):
        pass

    @abstractmethod
    def _showAll(self):
        pass

    def _rangeUpdated(self):
        self.rangeUpdatedSignal.emit(*self._range)

    def _dataUpdated(self):
        self.dataUpdatedSignal.emit()

    def _draw(self):
        self.predrawSignal.emit()
        self._fig.canvas.draw()
        self.postdrawSignal.emit()


# =============================================================================
# Single Image 
# =============================================================================
class BasicImg3Render(Img3RenderABC):
    # !todo: Ver si casa mejor arriba. Si lo pones arriba lo haces single Axis
    xlimChangedSignal = Qt.pyqtSignal(int, int)
    ylimChangedSignal = Qt.pyqtSignal(int, int)

    def __init__(self, figure, parent=None):
        super().__init__(figure, parent=parent)
        self._ax = self._fig.subplots()
        self._img = None
        self._imshow = None
        self._idx = None

        #########################################################
        # !todo: Crear una superclase para imagenes 2D y 3D
        # !todo: hacer que esto fuera configurable
        self._cmap = \
            createColorMap('cmc', [(0, 0, 0, 1), (0, 1, 0, 1)], N=255)

        self._plotParams = dict()
        self._plotParams['interpolation'] = 'nearest'
        self._plotParams['cmap'] = self._cmap
        self._fig.subplots_adjust(left=0.0, bottom=0.0,
                                  right=1.0, top=1.0)
        self._plotAxisConfig = \
            "self._ax.set_xticks([])\nself._ax.set_yticks([])\n"

        #########################################################
        self._ax.callbacks.connect('xlim_changed', self._onXlimsChange)
        self._ax.callbacks.connect('ylim_changed', self._onYlimsChange)



    def setPlotParams(self, **kwargs):
        self._plotParams = kwargs
        if not 'interpolation' in kwargs:
            self._plotParams['interpolation'] = 'nearest'
        if not 'cmap' in kwargs:
            self._plotParams['cmap'] = self._cmap

        if self.img is not None:
            print('set plot params')
            self._createNewPlot()

    def _onXlimsChange(self, ax):
        self.xlimChangedSignal.emit(*self._ax.get_xlim())

    def _onYlimsChange(self, ax):
        self.ylimChangedSignal.emit(*self._ax.get_ylim())

    def touch(self):
        self._updateData()

    @property
    def ax(self):
        return self._ax

    @property
    def xlim(self):
        return self._ax.get_xlim()

    @xlim.setter
    def xlim(self, value):
        if not (isinstance(value, tuple) and len(value) == 2 and \
                isinstance(value[0], num.Number) and \
                isinstance(value[0], num.Number)):
            raise TypeError("Tuple of numbers expected")

        l, r = self._ax.get_xlim()
        if l != value[0] or r != value[1]:
            self._ax.set_xlim(left=value[0], right=value[1])
            self._draw()

    @property
    def ylim(self):
        return self._ax.get_ylim()

    @ylim.setter
    def ylim(self, value):
        if not (isinstance(value, tuple) and len(value) == 2 and \
                isinstance(value[0], num.Number) and \
                isinstance(value[0], num.Number)):
            raise TypeError("Tuple of numbers expected")

        b, t = self._ax.get_ylim()
        if b != value[0] or t != value[1]:
            self._ax.set_ylim(bottom=value[0], top=value[1])
            self._draw()

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        if value is not None:
            if not isinstance(value, np.ndarray):
                raise TypeError("Numpy NDArray expected")
            elif 4 < len(value.shape) or len(value.shape) < 3:
                raise AttributeError("Not allowed shape")
            elif 4 == len(value.shape) and value.shape[-1] not in (3, 4):
                raise AttributeError("Not allowed color format")

        #        if type(value) != type(self._img) or np.any(value != self._img):
        if value is not self._img:
            self._img = value
            # self._createNewPlot()
            self._dataUpdated()

    def _createNewPlot(self):
        self._ax.clear()
        self._ax.callbacks.connect('xlim_changed', self._onXlimsChange)
        self._ax.callbacks.connect('ylim_changed', self._onYlimsChange)
        self._imshow = None

        self._updateRange()

        img = self._getPlotData()
        if img is not None:
            #############################################################################
            self._imshow = self._ax.imshow(img,
                                           **self._plotParams)

            exec(self._plotAxisConfig)
        #            self._updateMinMax()
        #############################################################################
        self._draw()

    def _updateData(self):
        if self._imshow is not None:
            img = self._getPlotData()
            if img is not None:
                self._imshow.set_data(img)
                #                self._updateMinMax()
                self._draw()

    def _updateRange(self):
        if self._img is None:
            self._range = (0, 0)
            slc = 0
        else:
            self._range = (0, self._img.shape[self._projPlane.value[0]] - 1)
            slc = int((self._range[0] + self._range[1]) // 2)
            # todo:poner más elegante
            self._slice = -1  # Hack para forzar la actualziación.

        self.sliceIdx = slc
        self._rangeUpdated()

    #    def _updateMinMax(self):
    #        if self._imshow is not None:
    #            if self._img is not None:
    #                mn = self._img.min()
    #                mx = self._img.max()
    #                self._imshow.set_clim(vmin = mn ,vmax = mx)

    def _getPlotData(self):
        if self._img is None: return None

        if self._showMP:
            img = self._img.max(axis=self._projPlane.value[0])
        else:
            img = self._img[self._idx]

        if self._projPlane.value[1]:
            if len(self._img.shape) == 4:
                img = img.transpose(1, 0, 2)
            else:
                img = img.transpose(1, 0)

        return img

    def _setSlice(self):
        if self._img is None:
            return
        else:
            idx = [slice(i) for i in self._img.shape]
            idx[self._projPlane.value[0]] = self._slice
            self._idx = tuple(idx)

            self._updateData()

    def _setProjetionPlane(self):
        self._createNewPlot()

    def _setMaximumProjection(self):
        self._updateData()

    def _zoomToData(self):
        if self._img is not None:
            if len(self._img.shape) == 3:
                img = self._img
            else:
                img = rgb2grayStack(self._img)

            mn, mx = getAABBImg(img)

            axis = self._projPlane.value[0]
            self.sliceIdx = int((mn[axis] + mx[axis]) // 2)

            v = [True, True, True]
            v[axis] = False

            mn = np.array(mn)[v]
            mx = np.array(mx)[v]

            if not self._projPlane.value[1]:
                mn = mn[::-1]
                mx = mx[::-1]

            self._ax.set_xlim(mn[0] - 0.5, mx[0] - 0.5)
            self._ax.set_ylim(mx[1] - 0.5, mn[1] - 0.5)
            self._draw()

    def _showAll(self):
        if self._img is not None:
            mx = self._img.shape[0:3]

            v = [True, True, True]
            v[self._projPlane.value[0]] = False

            mx = np.array(mx)[v]

            if self._projPlane.value[1]:
                mx = mx[::-1]

            self._ax.set_xlim(-0.5, mx[0] - 0.5)
            self._ax.set_ylim(mx[1] - 0.5, -0.5)
            self._draw()

if __name__ == '__main__':
    fig = plt.figure()  # plt.Figure()
    # add_axobserver, add_axis, execute_constrained_layout,get_axes, 
    # get_children(Artist),waitforbuttonpress,clear,contains,ginput,add_axobserver
    bi = BasicImg3Render(fig)
    bi.title = "Hola"

    #    img = np.arange(0,3*4*5*3).reshape(3,4,5,3)
    img = np.zeros((6, 6, 6, 3), dtype='uint8')
    img[2:5, 2:5, 2:5, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    bi.img = img

    print(bi.depthRange)
    print(bi.sliceIdx)

    bi.sliceIdx = 3
    bi.projectionPlane = Img3RenderABC.ProjectionPlane.XY
    #    bi.showMaximumProjection = True
    bi.zoomToData()
    bi.showAll()

    # fig.show()
