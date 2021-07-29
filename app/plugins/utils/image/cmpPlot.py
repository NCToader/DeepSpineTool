# -*- codifng: utf-8 -*-
"""
Created on Tue May  7 14:45:10 2019

@author: Marcos
"""

# https://matplotlib.org/gallery/userdemo/demo_gridspec05.html#sphx-glr-gallery-userdemo-demo-gridspec05-py
# https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
# https://matplotlib.org/tutorials/intermediate/tight_layout_guide.html#sphx-glr-tutorials-intermediate-tight-layout-guide-py
#
# https://stackoverflow.com/questions/15721094/detecting-mouse-event-in-an-image-with-matplotlib
#
# https://matplotlib.org/gallery/ticks_and_spines/tick-locators.html#sphx-glr-gallery-ticks-and-spines-tick-locators-py
#
# https://matplotlib.org/gallery/subplots_axes_and_figures/axes_margins.html#sphx-glr-gallery-subplots-axes-and-figures-axes-margins-py

import numpy as np
import copy

import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from app.plugins.utils.image.generic import isIterable
from app.plugins.utils.image.image import getAABBImg
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class CmpPlot:
    def __init__(self, *args,
                 supTitle=None,
                 title=None,
                 showMaxProj=True,
                 cmap=None,
                 widget=None,
                 **kwargs):
        '''
        Argumentos fijos
        ----------------
        *args: nplots, ncols
        *args: imgs

        Argumentos adicionales
        ----------------------
        Todos los parametros de la figura como: num, figsize=(6, 3), dpi=300
        '''

        assert 0 < len(args) < 3

        ############################################################
        ## Procesado de los parámetros de extension variable *ARGS
        ############################################################
        if isIterable(args[0]):
            self._img = args[0]
            self._nplots = len(args[0])
        else:
            self._nplots = args[0]
            # print (type(args[0]), flush=True)
            self._img = [None] * self._nplots

        if len(args) == 2:
            self._ncols = args[1]
        else:
            self._ncols = self._nplots

        ############################################################
        ## Atributos de clase
        ############################################################
        self._plot = [None] * self._nplots

        self._nrows = (self._nplots + self._ncols - 1) // self._ncols

        self.showMaxProj = showMaxProj

        if isIterable(title):
            self._title = copy.deepcopy(title)
        else:
            self._title = [copy.deepcopy(title)] * self._nplots

        if isIterable(cmap):
            self._cmap = copy.deepcopy(cmap)
        else:
            self._cmap = [copy.deepcopy(cmap)] * self._nplots

        ############################################################
        ## Creación de los subplots
        ############################################################
        self._fig, self._ax = plt.subplots(self._nrows, self._ncols,
                                           sharex=True, sharey=True,
                                           **kwargs)
        self._fig.canvas = FigureCanvas(self._fig)
        if not isinstance(self._ax, np.ndarray):
            self._ax = np.array([self._ax])

        self._fig.suptitle(supTitle)

        self._fig.subplots_adjust(left=0.1, bottom=0.24)

        ############################################################
        ## Slider
        ############################################################
        self._z = - 1
        self._buildSlider()

        ############################################################
        ## Checkbuttons
        ############################################################
        self._axShowMP = self._fig.add_axes([0.10, 0.04, 0.2, 0.15])

        self._ckBShowMP = CheckButtons(self._axShowMP,
                                       ['Show MP'],
                                       actives=[showMaxProj])

        self._ckBShowMP.on_clicked(self._ckBClicked)

        ############################################################
        ## Botones
        ############################################################
        self._axBtnZoom = self._fig.add_axes([0.70, 0.04, 0.2, 0.15])
        self._btnZoom = Button(self._axBtnZoom, 'Zoom to Data',
                               hovercolor='0.975')
        self._btnZoom.on_clicked(self._bntZoomClicked)

        self._axBtnReset = self._fig.add_axes([0.40, 0.04, 0.2, 0.15])
        self._btnReset = Button(self._axBtnReset, 'Reset',
                                hovercolor='0.975')
        self._btnReset.on_clicked(self._bntResetClicked)

        ############################################################
        ## Se construyen la imagenes
        ############################################################
        self._buildPlots()
        if widget is not None:
            widget.vl.addWidget(self._fig.canvas)
            self._fig.canvas.draw()
            toolbar = NavigationToolbar(self._fig.canvas, widget)
            widget.vl.addWidget(toolbar)

    def _bntResetClicked(self, event):
        if self._img[0] is not None:
            self._z = self._zInit
            self._sliderZ.set_val(self._z)

            self._ax.ravel()[0].set_xlim(0, self._img[0].shape[2])
            self._ax.ravel()[0].set_ylim(self._img[0].shape[1], 0)

    def _bntZoomClicked(self, val):
        if self._img[0] is not None:
            (mnz, mny, mnx), (mxz, mxy, mxx) = getAABBImg(self._img[0])

            #            print ((mnx, mny, mnz), (mxx, mxy, mxz),flush=True)
            self._z = (mxz - mnz) // 2
            self._sliderZ.set_val(self._z)

            self._ax.ravel()[0].set_xlim(mnx, mxx)
            self._ax.ravel()[0].set_ylim(mxy, mny)

    def _ckBClicked(self, val):
        self.showMaxProj = self._ckBShowMP.get_status()[0]
        for img, p in zip(self._img, self._plot):
            if p is not None:
                if self.showMaxProj is True:
                    p.set_data(np.max(img, axis=0))
                else:
                    p.set_data(img[int(self._z)])

        self._fig.canvas.draw_idle()

    #
    # def colorfunc(label):
    #    l.set_color(label)
    #    fig.canvas.draw_idle()
    # radio.on_clicked(colorfunc)

    def _buildSlider(self):
        self._zMax = np.min(
            [img.shape[0] for img in self._img if img is not None]) - 1
        self._zInit = self._zMax // 2

        if '_axZ' in vars(self):
            self._axZ.remove()

        self._axZ = self._fig.add_axes([0.10, 0.2, 0.8, 0.03],
                                       facecolor='lightgoldenrodyellow')
        self._sliderZ = Slider(self._axZ, 'Z',
                               0, self._zMax, valinit=self._zInit)  # borro argumento valstep=1

        if self._zMax < self._z or 0 > self._z:
            self._z = self._zInit

        self._sliderZ.set_val(self._z)
        self._sliderZ.on_changed(self._updateSlider)

    def _updateSlider(self, val):
        self._z = self._sliderZ.val

        if not self.showMaxProj:
            for img, p in zip(self._img, self._plot):
                if p is not None:
                    p.set_data(img[int(self._z)])

        self._fig.canvas.draw_idle()

    def _buildPlots(self):
        for idx, (img, cm, t, ax) in enumerate(zip(self._img, self._cmap,
                                                   self._title,
                                                   self._ax.ravel())):
            if img is None:
                continue

            if t is not None:
                ax.set_title(t)

            if self.showMaxProj:
                self._plot[idx] = ax.imshow(np.max(img, axis=0), cmap=cm,
                                            interpolation='nearest')
            else:
                self._plot[idx] = ax.imshow(img[int(self._z)], cmap=cm,
                                            interpolation='nearest')

            ax.set_xticks([])
            ax.set_yticks([])

    def addPlot(self, idx, plot, title=None, cmap=None):
        if title is not None:
            self._title[idx] = title

        if cmap is not None:
            self._title[idx] = cmap

        self._img[idx] = plot

        self._buildPlots()
        self._buildSlider()

    #
# plt.show()
