# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 16:47:23 2019

@author: Marcos García
"""

from PyQt5 import Qt
from skimage import exposure as skiex
import numpy as np

from app.plugins.ui.qbasics.lineEditEx import LineEditEx


class ContrastStrechingModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("contrastStrechingModifier_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            self.gc_widget = parent
            self.gc_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                           parent=parent)

            self.minper_widget = Qt.QWidget(parent=parent)
            self.minper_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                             Qt.QSizePolicy.Fixed)

            self.minper_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                               parent=self.minper_widget)
            self.minper_label = Qt.QLabel("Min percentil",
                                          parent=self.minper_widget)
            self.minper_lineEdit = LineEditEx(parent=self.minper_widget)
            self.minper_lineEdit.setIntFormat(mn=0, mx=99)
            self.minper_layout.addWidget(self.minper_label)
            self.minper_layout.addWidget(self.minper_lineEdit)

            self.maxper_widget = Qt.QWidget(parent=parent)
            self.maxper_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                             Qt.QSizePolicy.Fixed)

            self.maxper_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                               parent=self.maxper_widget)
            self.maxper_label = Qt.QLabel("Max percentil",
                                          parent=self.maxper_widget)
            self.maxper_lineEdit = LineEditEx(parent=self.maxper_widget)
            self.maxper_lineEdit.setIntFormat(mn=1, mx=100)
            self.maxper_layout.addWidget(self.maxper_label)
            self.maxper_layout.addWidget(self.maxper_lineEdit)

            self.apply_pushButton = Qt.QPushButton("Apply",
                                                   parent=parent)
            self.apply_pushButton.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                Qt.QSizePolicy.Fixed)
            self.apply_pushButton.setCheckable(True)
            self.apply_pushButton.setFlat(False)

            self.blank_widget = Qt.QWidget(parent=parent)
            self.blank_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                            Qt.QSizePolicy.Expanding)

            self.gc_layout.addWidget(self.minper_widget)
            self.gc_layout.addWidget(self.maxper_widget)
            self.gc_layout.addWidget(self.apply_pushButton)
            self.gc_layout.addWidget(self.blank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = ContrastStrechingModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None

        self._ui.apply_pushButton.toggled.connect(self._apply)
        self._ui.minper_lineEdit.valueChangedSignal.connect(self._adjustPer)
        self._ui.minper_lineEdit.valueChangedSignal.connect(self._adjustPer)

    def _resetUI(self):
        self._ui.apply_pushButton.blockSignals(True)
        self._ui.apply_pushButton.setChecked(False)
        self._ui.apply_pushButton.blockSignals(False)

        self._ui.minper_lineEdit.value = 2
        self._ui.maxper_lineEdit.value = 98

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
        self._viewer.cbLoopThread.setCallback(self._adjustCM)

    @staticmethod
    def _adjustCM(editor, img, apply, mn, mx):
        if apply:
            pmn, pmx = np.percentile(img, (mn, mx))
            editor.img = skiex.rescale_intensity(img, in_range=(pmn, pmx))
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
                                                False, 2, 98)

    @Qt.pyqtSlot()
    def _adjustPer(self):
        if self._initialImg is None:
            self._setInitialValues()

        if self._ui.minper_lineEdit.value >= self._ui.maxper_lineEdit.value:
            if self.sender() is self._ui.minper_lineEdit:
                self._ui.maxper_lineEdit.value = \
                    self._ui.minper_lineEdit.value + 1
            else:
                self._ui.minper_lineEdit.value = \
                    self._ui.maxper_lineEdit.value - 1

        self._adjust()

    def _adjust(self):
        if self._ui.apply_pushButton.isChecked():
            self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                                True,
                                                self._ui.minper_lineEdit.value,
                                                self._ui.maxper_lineEdit.value)
