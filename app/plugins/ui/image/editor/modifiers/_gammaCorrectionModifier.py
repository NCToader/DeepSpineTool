# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:18:12 2019

@author: Marcos Garcia
"""

from PyQt5 import Qt
from skimage import exposure as skiex


class GammaCorrectionModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("gammaCorrectionModifier_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            self.gc_widget = parent
            self.gc_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                           parent=parent)

            self.gamma_slider = Qt.QSlider(parent=parent)
            self.gamma_slider.setOrientation(Qt.Qt.Horizontal)
            self.gamma_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                            Qt.QSizePolicy.Fixed)
            self.gamma_slider.setMinimum(-1000)
            self.gamma_slider.setMaximum(1000)
            self.gamma_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.gamma_slider.setTickInterval(1000)
            self.gamma_label = Qt.QLabel("Gamma",
                                         parent=parent)
            self.gamma_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                           Qt.QSizePolicy.Fixed)

            self.gain_slider = Qt.QSlider(parent=parent)
            self.gain_slider.setOrientation(Qt.Qt.Horizontal)
            self.gain_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                           Qt.QSizePolicy.Fixed)
            self.gain_slider.setMinimum(-1000)
            self.gain_slider.setMaximum(1000)
            self.gain_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.gain_slider.setTickInterval(1000)
            self.gain_label = Qt.QLabel("Gain",
                                        parent=parent)
            self.gain_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                          Qt.QSizePolicy.Fixed)

            self.blank_widget = Qt.QWidget(parent=parent)
            self.blank_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                            Qt.QSizePolicy.Expanding)

            self.gc_layout.addWidget(self.gamma_label)
            self.gc_layout.addWidget(self.gamma_slider)
            self.gc_layout.addWidget(self.gain_label)
            self.gc_layout.addWidget(self.gain_slider)
            self.gc_layout.addWidget(self.blank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = GammaCorrectionModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None
        self._maxGamma = 6.0

        self._ui.gamma_slider.valueChanged.connect(self._adjust)
        self._ui.gain_slider.valueChanged.connect(self._adjust)

    def _resetSliders(self):
        self._ui.gamma_slider.blockSignals(True)
        self._ui.gamma_slider.setValue(0)
        self._ui.gamma_slider.blockSignals(False)
        self._ui.gain_slider.blockSignals(True)
        self._ui.gain_slider.setValue(0)
        self._ui.gain_slider.blockSignals(False)

    def update(self):
        self._resetSliders()
        self._initialImg = None

    def reset(self):
        self.update()

    @property
    def changed(self):
        return self._ui.gain_slider.value() != 0 or \
               self._ui.gamma_slider.value() != 0

    def _setInitialValues(self):
        self._resetSliders()

        if self._viewer.initialImg is None:
            return

        self._initialImg = self._viewer.initialImg
        self._viewer.cbLoopThread.setCallback(self._adjustGamma)

    @staticmethod
    def _adjustGamma(editor, img, gamma, gain):
        editor.img = skiex.adjust_gamma(img, gamma=gamma, gain=gain)

    @Qt.pyqtSlot()
    def _adjust(self):
        if self._initialImg is None:
            self._setInitialValues()

        gm = self._ui.gamma_slider.value() / 1000
        gm = gm * self._maxGamma
        gm = 1.0 / (1.0 - gm) if gm < 0 else gm + 1

        gn = self._ui.gain_slider.value() / 1000
        gn = 1.02 * (1 + gn) / (1.02 - gn)

        self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                            gm, gn)
