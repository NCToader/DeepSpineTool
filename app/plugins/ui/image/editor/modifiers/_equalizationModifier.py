# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 13:05:09 2019

@author: Marcos García
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
from skimage import exposure as skiex
import numpy as np

from app.plugins.ui.qbasics.lineEditEx import LineEditEx


class EqualizationModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("equalizationModifier_form")
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
            self.gc_layout.addWidget(self.apply_pushButton)
            self.gc_layout.addWidget(self.blank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = EqualizationModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None

        self._ui.apply_pushButton.toggled.connect(self._apply)
        self._ui.nbin_lineEdit.valueChangedSignal.connect(self._adjust)

    def _resetUI(self):
        self._ui.apply_pushButton.blockSignals(True)
        self._ui.apply_pushButton.setChecked(False)
        self._ui.apply_pushButton.blockSignals(False)

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
    def _adjustEq(editor, img, apply, nbins):
        if apply:
            print(img.max(), img.min())
            editor.img = skiex.rescale_intensity(
                skiex.equalize_hist(img, nbins=nbins),
                out_range=editor.realRange).astype(img.dtype)
            print(editor.img.max(), editor.img.min())
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
                                                False, 256)

    @Qt.pyqtSlot()
    def _adjust(self):
        if self._initialImg is None:
            self._setInitialValues()

        if self._ui.apply_pushButton.isChecked():
            nb = self._ui.nbin_lineEdit.value
            print(nb)

            self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                                True, nb)
