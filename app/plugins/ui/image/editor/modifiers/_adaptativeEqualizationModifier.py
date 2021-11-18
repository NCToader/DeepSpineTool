# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 17:26:31 2019

@author: Marcos García
"""
from PyQt5 import Qt
from skimage import exposure as skiex
import numpy as np

from app.plugins.ui.qbasics.lineEditEx import LineEditEx


class AdaptativeEqualizationModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("adaptativeEqualizationModifier_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            self.gc_widget = parent
            self.gc_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                           parent=parent)

            self.nbin_widget = Qt.QWidget(parent=parent)
            self.nbin_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                           Qt.QSizePolicy.Fixed)

            self.nbin_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                             parent=self.nbin_widget)
            self.nbin_label = Qt.QLabel("Nº of bins:",
                                        parent=self.nbin_widget)
            self.nbin_lineEdit = LineEditEx(parent=self.nbin_widget)
            self.nbin_lineEdit.setIntFormat(mn=2, mx=np.iinfo('uint16').max)
            self.nbin_layout.addWidget(self.nbin_label)
            self.nbin_layout.addWidget(self.nbin_lineEdit)

            self.clip_slider = Qt.QSlider(parent=parent)
            self.clip_slider.setOrientation(Qt.Qt.Horizontal)
            self.clip_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                           Qt.QSizePolicy.Fixed)
            self.clip_slider.setMinimum(1)
            self.clip_slider.setMaximum(1000)
            self.clip_slider.setTickPosition(Qt.QSlider.NoTicks)
            self.clip_label = Qt.QLabel("Clip limit",
                                        parent=parent)
            self.clip_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                          Qt.QSizePolicy.Fixed)

            self.size_slider = Qt.QSlider(parent=parent)
            self.size_slider.setOrientation(Qt.Qt.Horizontal)
            self.size_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                           Qt.QSizePolicy.Fixed)
            self.size_slider.setMinimum(1)
            self.size_slider.setMaximum(16)
            self.size_slider.setTickPosition(Qt.QSlider.NoTicks)
            self.size_label = Qt.QLabel("Patch Size",
                                        parent=parent)
            self.size_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                          Qt.QSizePolicy.Fixed)

            self.apply_pushButton = Qt.QPushButton("Apply",
                                                   parent=parent)
            self.apply_pushButton.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                Qt.QSizePolicy.Fixed)
            self.apply_pushButton.setCheckable(True)
            self.apply_pushButton.setFlat(False)

            self.blank_widget = Qt.QWidget(parent=parent)
            self.blank_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                            Qt.QSizePolicy.Expanding)

            self.gc_layout.addWidget(self.nbin_widget)
            self.gc_layout.addWidget(self.size_label)
            self.gc_layout.addWidget(self.size_slider)
            self.gc_layout.addWidget(self.clip_label)
            self.gc_layout.addWidget(self.clip_slider)
            self.gc_layout.addWidget(self.apply_pushButton)
            self.gc_layout.addWidget(self.blank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = AdaptativeEqualizationModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None

        self._ui.apply_pushButton.toggled.connect(self._apply)
        self._ui.nbin_lineEdit.valueChangedSignal.connect(self._adjust)
        self._ui.size_slider.valueChanged.connect(self._adjust)
        self._ui.clip_slider.valueChanged.connect(self._adjust)

    def _resetUI(self):
        self._ui.apply_pushButton.blockSignals(True)
        self._ui.apply_pushButton.setChecked(False)
        self._ui.apply_pushButton.blockSignals(False)

        self._ui.clip_slider.blockSignals(True)
        self._ui.clip_slider.setValue(10)
        self._ui.clip_slider.blockSignals(False)

        self._ui.size_slider.blockSignals(True)
        self._ui.size_slider.setValue(8)
        self._ui.size_slider.blockSignals(False)

        self._ui.nbin_lineEdit.value = 256
        self._ui.nbin_lineEdit.setEnabled(False)

    def update(self):
        self._resetUI()
        self._initialImg = None

    def reset(self):
        self.update()

    @property
    def changed(self):
        return self._ui.apply_pushButton.isChecked()

    def _setInitialValues(self):
        self._resetUI()

        if self._viewer.initialImg is None:
            return

        self._initialImg = self._viewer.initialImg
        self._viewer.cbLoopThread.setCallback(self._adjustEq)

        if np.issubdtype(self._initialImg.dtype, np.floating):
            self._ui.nbin_lineEdit.setEnabled(True)

    @staticmethod
    def _adjustEq(editor, img, apply, size, clip, nbins):
        if apply:

            outImg = np.zeros(img.shape)

            print(img.shape, size, clip, nbins, img[2, :, :].shape)

            for i in range(img.shape[0]):
                outImg[i] = skiex.rescale_intensity(
                    skiex.equalize_adapthist(img[i],
                                             kernel_size=size,
                                             clip_limit=clip,
                                             nbins=nbins),
                    out_range=editor.realRange).astype(img.dtype)

            editor.img = outImg
        else:
            editor.img = img

    @Qt.pyqtSlot()
    def _apply(self):
        if self._initialImg is None:
            self._setInitialValues()

            self._ui.apply_pushButton.blockSignals(True)
            self._ui.apply_pushButton.setChecked(True)
            self._ui.apply_pushButton.blockSignals(False)

        if self._ui.apply_pushButton.isChecked():
            self._adjust()
        else:
            self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                                False, 1, 1, 256)

    @Qt.pyqtSlot()
    def _adjust(self):
        if self._initialImg is None:
            self._setInitialValues()

        if self._ui.apply_pushButton.isChecked():
            nb = self._ui.nbin_lineEdit.value
            s = 16 - self._ui.size_slider.value()
            s = tuple(np.array(self._initialImg.shape[1:3]) // s)
            c = self._ui.clip_slider.value() / 1000

            self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                                True, s, c, nb)
