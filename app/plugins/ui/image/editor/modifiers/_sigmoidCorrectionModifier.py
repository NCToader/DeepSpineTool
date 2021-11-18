# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 19:42:22 2019

@author: Marcos García
"""

from PyQt5 import Qt
from skimage import exposure as skiex


class SigmoidCorrectionModifier(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            # Main Widgets
            #############################################
            parent.setObjectName("sigmoidCorrectionModifier_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            self.gc_widget = parent
            self.gc_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                           parent=parent)

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

            self.cutoff_slider = Qt.QSlider(parent=parent)
            self.cutoff_slider.setOrientation(Qt.Qt.Horizontal)
            self.cutoff_slider.setSizePolicy(Qt.QSizePolicy.Expanding,
                                             Qt.QSizePolicy.Fixed)
            self.cutoff_slider.setMinimum(-1000)
            self.cutoff_slider.setMaximum(1000)
            self.cutoff_slider.setTickPosition(Qt.QSlider.TicksBothSides)
            self.cutoff_slider.setTickInterval(1000)
            self.cutoff_label = Qt.QLabel("Cut off",
                                          parent=parent)
            self.cutoff_label.setSizePolicy(Qt.QSizePolicy.Fixed,
                                            Qt.QSizePolicy.Fixed)

            self.inverse_checkBox = Qt.QCheckBox(
                "Inverse logarithmic correction",
                parent=parent)
            self.inverse_checkBox.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                Qt.QSizePolicy.Fixed)

            self.apply_pushButton = Qt.QPushButton("Apply",
                                                   parent=parent)
            self.apply_pushButton.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                Qt.QSizePolicy.Fixed)
            self.apply_pushButton.setCheckable(True)
            self.apply_pushButton.setFlat(False)

            self.logBlank_widget = Qt.QWidget(parent=parent)
            self.logBlank_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                               Qt.QSizePolicy.Expanding)

            self.gc_layout.addWidget(self.cutoff_label)
            self.gc_layout.addWidget(self.cutoff_slider)
            self.gc_layout.addWidget(self.gain_label)
            self.gc_layout.addWidget(self.gain_slider)
            self.gc_layout.addWidget(self.inverse_checkBox)
            self.gc_layout.addWidget(self.apply_pushButton)
            self.gc_layout.addWidget(self.logBlank_widget)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)

        self._ui = SigmoidCorrectionModifier._UI(parent=self)
        self._viewer = viewer
        self._initialImg = None

        self._ui.cutoff_slider.valueChanged.connect(self._adjust)
        self._ui.inverse_checkBox.stateChanged.connect(self._adjust)
        self._ui.gain_slider.valueChanged.connect(self._adjust)
        self._ui.apply_pushButton.toggled.connect(self._apply)

    def _resetUI(self):
        self._ui.inverse_checkBox.blockSignals(True)
        self._ui.inverse_checkBox.setCheckState(Qt.Qt.Unchecked)
        self._ui.inverse_checkBox.blockSignals(False)

        self._ui.apply_pushButton.blockSignals(True)
        self._ui.apply_pushButton.setChecked(False)
        self._ui.apply_pushButton.blockSignals(False)

        self._ui.gain_slider.blockSignals(True)
        self._ui.gain_slider.setValue(0)
        self._ui.gain_slider.blockSignals(False)

        self._ui.cutoff_slider.blockSignals(True)
        self._ui.cutoff_slider.setValue(0)
        self._ui.cutoff_slider.blockSignals(False)

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
        self._viewer.cbLoopThread.setCallback(self._adjustSigmoid)

    @staticmethod
    def _adjustSigmoid(editor, img, apply, inv, cutoff, gain):
        if apply:
            editor.img = skiex.adjust_sigmoid(img, cutoff=cutoff,
                                              gain=gain, inv=inv)
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
                                                False, False, 0.5, 10.0)

    @Qt.pyqtSlot()
    def _adjust(self):
        if self._initialImg is None:
            self._setInitialValues()

        if self._ui.apply_pushButton.isChecked():
            i = self._ui.inverse_checkBox.checkState() == Qt.Qt.Checked
            c = (self._ui.cutoff_slider.value() + 1000) / 2000.0

            g = self._ui.gain_slider.value() / 1000.0
            #            g = 1.02 * (1 + g) / (1.02 - g)
            g = 10.2 * (1 + g) / (1.02 - g)

            self._viewer.cbLoopThread.requestCB(self._viewer, self._initialImg,
                                                True, i, c, g)
