# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 18:57:37 2019

@author: Marcos García
"""
from PyQt5 import Qt
import numpy as np


class ContrastBrightnessModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("contrastBrightnessEditor_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            self.cnBr_widget = parent
            self.cnBr_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,

                                             parent=parent)
            self.contrast_slider = Qt.QSlider(parent=parent)
            self.contrast_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                               Qt.QSizePolicy.Fixed)

            self.contrast_slider.setOrientation(Qt.Qt.Horizontal)
            self.contrast_slider.setMinimum(-100)
            self.contrast_slider.setMaximum(100)
            self.contrast_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.contrast_slider.setTickInterval(100)
            self.contrast_label = Qt.QLabel("Contrast",

                                            parent=parent)
            self.contrast_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                              Qt.QSizePolicy.Fixed)

            self.midContrast_slider = Qt.QSlider(parent=parent)
            self.midContrast_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                                  Qt.QSizePolicy.Fixed)

            self.midContrast_slider.setOrientation(Qt.Qt.Horizontal)
            self.midContrast_slider.setMinimum(-100)
            self.midContrast_slider.setMaximum(100)
            self.midContrast_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.midContrast_slider.setTickInterval(100)
            self.midContrast_label = Qt.QLabel("Mid contrast value",

                                               parent=parent)
            self.midContrast_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                 Qt.QSizePolicy.Fixed)

            self.brightness_slider = Qt.QSlider(parent=parent)
            self.brightness_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                                 Qt.QSizePolicy.Fixed)

            self.brightness_slider.setOrientation(Qt.Qt.Horizontal)
            self.brightness_slider.setMinimum(-100)
            self.brightness_slider.setMaximum(100)
            self.brightness_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.brightness_slider.setTickInterval(100)
            self.brightness_label = Qt.QLabel("Brightness",

                                              parent=parent)
            self.brightness_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                Qt.QSizePolicy.Fixed)

            self.keepImgRange_checkBox = Qt.QCheckBox(
                "Keep image range",
                parent=parent)
            self.keepImgRange_checkBox.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                     Qt.QSizePolicy.Fixed)

            self.cnBrBlank_widget = Qt.QWidget(parent=parent)
            self.cnBrBlank_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                                Qt.QSizePolicy.Expanding)

            self.cnBr_layout.addWidget(self.contrast_label)
            self.cnBr_layout.addWidget(self.contrast_slider)
            self.cnBr_layout.addWidget(self.midContrast_label)
            self.cnBr_layout.addWidget(self.midContrast_slider)
            self.cnBr_layout.addWidget(self.brightness_label)
            self.cnBr_layout.addWidget(self.brightness_slider)
            self.cnBr_layout.addWidget(self.keepImgRange_checkBox)

            self.cnBr_layout.addWidget(self.cnBrBlank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = ContrastBrightnessModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None

        self._ui.contrast_slider.valueChanged.connect(self._adjust)
        self._ui.midContrast_slider.valueChanged.connect(self._adjust)
        self._ui.brightness_slider.valueChanged.connect(self._adjust)
        self._ui.keepImgRange_checkBox.stateChanged.connect(
            self._keepImgRange)

    def _resetSliders(self):
        self._ui.contrast_slider.blockSignals(True)
        self._ui.midContrast_slider.blockSignals(True)
        self._ui.brightness_slider.blockSignals(True)
        self._ui.contrast_slider.setValue(0)
        self._ui.midContrast_slider.setValue(0)
        self._ui.brightness_slider.setValue(0)
        self._ui.contrast_slider.blockSignals(False)
        self._ui.midContrast_slider.blockSignals(False)
        self._ui.brightness_slider.blockSignals(False)

    def update(self):
        self._resetSliders()
        self._initialImg = None

        self._imgType = None
        self._minValue = None
        self._maxValue = None

    def reset(self):
        self.update()

    @property
    def changed(self):
        return not (self._ui.contrast_slider.value() == 0 and \
                    self._ui.midContrast_slider.value() == 0 and \
                    self._ui.brightness_slider.value() == 0)

    def _setInitialValues(self):
        self._resetSliders()

        if self._viewer.initialImg is None:
            return

        self._initialImg = self._viewer.initialImg
        self._imgType = self._initialImg.dtype

        if self._ui.keepImgRange_checkBox.checkState() == Qt.Qt.Unchecked:
            self._minValue, self._maxValue = self._viewer.realRange
        else:
            self._minValue, self._maxValue = self._viewer.imgRange

        self._viewer.cbLoopThread.setCallback(self._adjustCntBrg)

    @Qt.pyqtSlot()
    def _keepImgRange(self):
        self._setInitialValues()
        self._adjust()

    @staticmethod
    def _adjustCntBrg(editor, img, cv, mv, bv, minv, maxv, dtype):
        editor.img = np.clip((img - mv) * cv + bv, minv, maxv). \
            astype(dtype)

    @Qt.pyqtSlot()
    def _adjust(self):
        if self._initialImg is None:
            self._setInitialValues()

        cv = self._ui.contrast_slider.value() / 100
        cv = 1.02 * (1 + cv) / (1.02 - cv)
        mv = self._ui.midContrast_slider.value() / 200 + 0.5
        mv = self._maxValue * mv + self._minValue * (1 - mv)
        bv = self._ui.brightness_slider.value() / 100
        bv = bv * (self._maxValue - self._minValue) + mv

        #        self._adjustCntBrg(self._viewer, self._initialImg,
        #                           cv, mv, bv,
        #                           self._minValue, self._maxValue, self._imgType)
        self._viewer.cbLoopThread.requestCB(
            self._viewer, self._initialImg, cv, mv, bv,
            self._minValue, self._maxValue, self._imgType)
