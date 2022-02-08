# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:45:30 2019

@author: Marcos García
todo: Usar https://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.rescale_intensity
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
import numpy as np

from app.plugins.ui.image.editor.modifiers.ui_scaling import Ui_scaling_widget
from app.plugins.ui.qbasics.lineEditEx import LineEditEx


class ScalingModifier(Qt.QWidget):
    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._ui = Ui_scaling_widget()
        self._ui.setupUi(self)

        self._viewer = viewer
        self._initialImg = None

        le = LineEditEx()
        self._ui.customInputRange_widget.layout().replaceWidget(
            self._ui.minInputValue_lineEdit, le)
        self._ui.minInputValue_lineEdit.deleteLater()
        self._ui.minInputValue_lineEdit = le
        le = LineEditEx()
        self._ui.customInputRange_widget.layout().replaceWidget(
            self._ui.maxInputValue_lineEdit, le)
        self._ui.maxInputValue_lineEdit.deleteLater()
        self._ui.maxInputValue_lineEdit = le

        le = LineEditEx()
        self._ui.customOutputRange_widget.layout().replaceWidget(
            self._ui.minOutputValue_lineEdit, le)
        self._ui.minOutputValue_lineEdit.deleteLater()
        self._ui.minOutputValue_lineEdit = le
        le = LineEditEx()
        self._ui.customOutputRange_widget.layout().replaceWidget(
            self._ui.maxOutputValue_lineEdit, le)
        self._ui.maxOutputValue_lineEdit.deleteLater()
        self._ui.maxOutputValue_lineEdit = le

        le = LineEditEx()
        self._ui.customAverage_widget.layout().replaceWidget(
            self._ui.average_lineEdit, le)
        self._ui.average_lineEdit.deleteLater()
        self._ui.average_lineEdit = le
        le = LineEditEx()
        self._ui.customAverage_widget.layout().replaceWidget(
            self._ui.stdDevValue_lineEdit, le)
        self._ui.stdDevValue_lineEdit.deleteLater()
        self._ui.stdDevValue_lineEdit = le

        self._reset()

        self._ui.none_radioButton.clicked.connect(self._scalingMethodChanged)
        self._ui.normalization_radioButton.clicked.connect(
            self._scalingMethodChanged)
        self._ui.meanNormamalization_radioButton.clicked.connect(
            self._scalingMethodChanged)
        self._ui.standarization_radioButton.clicked.connect(
            self._scalingMethodChanged)

        self._ui.selectCustomAverage_checkBox.clicked.connect(
            self._checkBntChanged)
        self._ui.selectInputRange_checkBox.clicked.connect(
            self._checkBntChanged)
        self._ui.selectOuptutRange_checkBox.clicked.connect(
            self._checkBntChanged)

        self._ui.keepDataTypes_radioButton.clicked.connect(self._outputChanged)
        self._ui.keepRange_radioButton.clicked.connect(self._outputChanged)
        self._ui.convertToReal_radioButton.clicked.connect(self._outputChanged)

        self._ui.minInputValue_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)
        self._ui.maxInputValue_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)
        self._ui.minOutputValue_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)
        self._ui.maxOutputValue_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)
        self._ui.average_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)
        self._ui.stdDevValue_lineEdit.valueChangedSignal.connect(
            self._lineEditChanged)

    def _reset(self):
        self._ui.none_radioButton.setChecked(True)
        self._ui.keepDataTypes_radioButton.setChecked(True)

        self._ui.selectCustomAverage_checkBox.setChecked(False)
        self._ui.selectInputRange_checkBox.setChecked(False)
        self._ui.selectOuptutRange_checkBox.setChecked(False)

        self._ui.minInputValue_lineEdit.setStringFormat()
        self._ui.maxInputValue_lineEdit.setStringFormat()
        self._ui.minOutputValue_lineEdit.setStringFormat()
        self._ui.maxOutputValue_lineEdit.setStringFormat()
        self._ui.average_lineEdit.setStringFormat()
        self._ui.stdDevValue_lineEdit.setStringFormat()

        self._ui.minInputValue_lineEdit.value = ""
        self._ui.maxInputValue_lineEdit.value = ""
        self._ui.minOutputValue_lineEdit.value = ""
        self._ui.maxOutputValue_lineEdit.value = ""
        self._ui.average_lineEdit.value = ""
        self._ui.stdDevValue_lineEdit.value = ""

        self._ui.customAverage_widget.hide()
        self._ui.customInputRange_widget.hide()
        self._ui.customOutputRange_widget.hide()

        self._initialImg = None
        self._scalingMethodChanged()

    @Qt.pyqtSlot()
    def _scalingMethodChanged(self):
        print("Method change")

        if self._viewer.initialImg is None:
            self._ui.none_radioButton.setChecked(True)
            self._ui.input_widget.hide()
            self._ui.average_widget.hide()
            self._ui.output_widget.hide()
            return

        if self._ui.none_radioButton.isChecked():
            self._ui.input_widget.hide()
            self._ui.average_widget.hide()
            self._ui.output_widget.hide()

        elif self._ui.normalization_radioButton.isChecked():
            self._ui.input_widget.show()
            self._ui.average_widget.hide()
            self._ui.output_widget.show()

            if self._ui.selectInputRange_checkBox.isChecked() and \
                    self._ui.selectInputRange_checkBox.isChecked():
                self._ui.keepRange_radioButton.hide()
                self._ui.keepDataTypes_radioButton.setChecked(True)
            else:
                self._ui.keepRange_radioButton.show()

        elif self._ui.meanNormamalization_radioButton.isChecked():
            self._ui.input_widget.show()
            self._ui.average_widget.show()
            self._ui.output_widget.show()

            self._ui.keepRange_radioButton.show()

            self._ui.stdDevValue_label.hide()
            self._ui.stdDevValue_lineEdit.hide()

        elif self._ui.standarization_radioButton.isChecked():
            self._ui.input_widget.hide()
            self._ui.average_widget.show()
            self._ui.output_widget.show()

            self._ui.keepRange_radioButton.show()

            self._ui.stdDevValue_label.show()
            self._ui.stdDevValue_lineEdit.show()

        if self._initialImg is None:
            self._setInitialValues()

        self._scale()

    @Qt.pyqtSlot()
    def _outputChanged(self):
        print("Output")
        if self._viewer.initialImg is None:
            self._ui.keepDataTypes_radioButton.setChecked(True)
            self._ui.outputRange_widget.show()
            return

        if self._ui.keepDataTypes_radioButton.isChecked():
            self._ui.outputRange_widget.show()
        elif self._ui.keepRange_radioButton.isChecked():
            self._ui.outputRange_widget.hide()
        elif self._ui.convertToReal_radioButton.isChecked():
            self._ui.outputRange_widget.show()

        if self._initialImg is None:
            self._setInitialValues()
        else:
            if self._ui.keepDataTypes_radioButton.isChecked():
                self._ui.minOutputValue_lineEdit.setIntFormat(
                    mn=int(self._rmn), mx=int(self._rmx) - 1)
                self._ui.maxOutputValue_lineEdit.setIntFormat(
                    mn=int(self._rmn) + 1, mx=int(self._rmx))

                self._ui.minOutputValue_lineEdit.value = int(self._rmn)
                self._ui.maxOutputValue_lineEdit.value = int(self._rmx)

            elif self._ui.convertToReal_radioButton.isChecked():

                self._ui.minOutputValue_lineEdit.setFloatFormat()
                #                        mn = float(self._rmn), mx = float(self._rmx))
                self._ui.maxOutputValue_lineEdit.setFloatFormat()
                #                        mn = float(self._rmn), mx = float(self._rmx))

                self._ui.minOutputValue_lineEdit.value = float(self._rmn)
                self._ui.maxOutputValue_lineEdit.value = float(self._rmx)

        self._scale()

    @Qt.pyqtSlot()
    def _lineEditChanged(self):
        print("Line Edit")
        if self._viewer.initialImg is None:
            self._ui.minInputValue_lineEdit.setStringFormat()
            self._ui.maxInputValue_lineEdit.setStringFormat()
            self._ui.minOutputValue_lineEdit.setStringFormat()
            self._ui.maxOutputValue_lineEdit.setStringFormat()
            self._ui.average_lineEdit.setStringFormat()
            self._ui.stdDevValue_lineEdit.setStringFormat()

            self._ui.minInputValue_lineEdit.value = ""
            self._ui.maxInputValue_lineEdit.value = ""
            self._ui.minOutputValue_lineEdit.value = ""
            self._ui.maxOutputValue_lineEdit.value = ""
            self._ui.average_lineEdit.value = ""
            self._ui.stdDevValue_lineEdit.value = ""
            return

        if self._initialImg is None:
            self._setInitialValues()

        if self._ui.minInputValue_lineEdit.value >= \
                self._ui.maxInputValue_lineEdit.value:
            if self._ui.minInputValue_lineEdit is self.sender():
                self._ui.minInputValue_lineEdit.value = \
                    self._ui.maxInputValue_lineEdit.value
            else:
                self._ui.maxInputValue_lineEdit.value = \
                    self._ui.minInputValue_lineEdit.value

        elif self._ui.minOutputValue_lineEdit.value >= \
                self._ui.maxOutputValue_lineEdit.value:
            if self._ui.minOutputValue_lineEdit is self.sender():
                self._ui.minOutputValue_lineEdit.value = \
                    self._ui.maxOutputValue_lineEdit.value
            else:
                self._ui.maxOutputValue_lineEdit.value = \
                    self._ui.minOutputValue_lineEdit.value

        self._scale()

    @Qt.pyqtSlot()
    def _checkBntChanged(self):
        print("Range ...")

        if self._viewer.initialImg is None:
            self._ui.selectCustomAverage_checkBox.setChecked(False)
            self._ui.selectInputRange_checkBox.setChecked(False)
            self._ui.selectOuptutRange_checkBox.setChecked(False)
            return

        if self._initialImg is None:
            self._setInitialValues()

        self._scale()

    def _setInitialValues(self):
        self._viewer.cbLoopThread.setCallback(self._scaling)

        self._initialImg = self._viewer.initialImg
        self._dtype = self._initialImg.dtype

        self._rmn, self._rmx = self._viewer.realRange
        self._imn, self._imx = self._viewer.imgRange

        self._imean = self._initialImg.mean()
        self._istd = self._initialImg.std()

        if np.issubdtype(self._dtype, np.integer):
            self._ui.minInputValue_lineEdit.setIntFormat(
                mn=self._rmn, mx=self._rmx - 1)
            self._ui.maxInputValue_lineEdit.setIntFormat(
                mn=self._rmn + 1, mx=self._rmx)

            self._ui.minInputValue_lineEdit.value = int(self._rmn)
            self._ui.maxInputValue_lineEdit.value = int(self._rmx)

        elif np.issubdtype(self._dtype, np.float):
            self._ui.minInputValue_lineEdit.setFloatFormat(
                mn=self._rmn, mx=self._rmx - 1)
            self._ui.maxInputValue_lineEdit.setFloatFormat(
                mn=self._rmn + 1, mx=self._rmx)

            self._ui.minInputValue_lineEdit.value = float(self._rmn)
            self._ui.maxInputValue_lineEdit.value = float(self._rmx)

        self._ui.average_lineEdit.setFloatFormat(
            mn=float(self._rmn), mx=float(self._rmx))
        self._ui.stdDevValue_lineEdit.setFloatFormat(
            mn=0.5e-10, mx=float(self._rmx) - float(self._rmn))

        self._ui.average_lineEdit.value = float(self._imean)
        self._ui.stdDevValue_lineEdit.value = float(self._istd)

        if self._ui.keepDataTypes_radioButton.isChecked():
            self._ui.minOutputValue_lineEdit.setIntFormat(
                mn=int(self._rmn), mx=int(self._rmx) - 1)
            self._ui.maxOutputValue_lineEdit.setIntFormat(
                mn=int(self._rmn) + 1, mx=int(self._rmx))

            self._ui.minOutputValue_lineEdit.value = int(self._rmn)
            self._ui.maxOutputValue_lineEdit.value = int(self._rmx)

        elif self._ui.convertToReal_radioButton.isChecked():

            self._ui.minOutputValue_lineEdit.setFloatFormat()
            #                    mn = float(self._rmn), mx = float(self._rmx))
            self._ui.maxOutputValue_lineEdit.setFloatFormat()
            #                    mn = float(self._rmn), mx = float(self._rmx))

            self._ui.minOutputValue_lineEdit.value = float(self._rmn)
            self._ui.maxOutputValue_lineEdit.value = float(self._rmx)

    def update(self):
        self._reset()
        self._initialImg = None

    def reset(self):
        self.update()

    @property
    def changed(self):
        print(self._ui.none_radioButton.isChecked())
        return not self._ui.none_radioButton.isChecked()

    def _scale(self):
        kwargs = dict()

        if self._ui.none_radioButton.isChecked():
            self._viewer.cbLoopThread.requestCB(
                self._viewer, self._initialImg, scalingMethod="reset")
            return

        elif self._ui.normalization_radioButton.isChecked():
            scalingMethod = "norm"

            if self._ui.selectInputRange_checkBox.isChecked():
                if self._ui.minInputValue_lineEdit.value == \
                        self._ui.maxInputValue_lineEdit.value:
                    return
                kwargs['imn'] = self._ui.minInputValue_lineEdit.value
                kwargs['imx'] = self._ui.maxInputValue_lineEdit.value
            else:
                kwargs['imn'] = self._imn
                kwargs['imx'] = self._imx

        elif self._ui.meanNormamalization_radioButton.isChecked():
            scalingMethod = "mnorm"

            if self._ui.selectInputRange_checkBox.isChecked():
                if self._ui.minInputValue_lineEdit.value == \
                        self._ui.maxInputValue_lineEdit.value:
                    return
                kwargs['imn'] = self._ui.minInputValue_lineEdit.value
                kwargs['imx'] = self._ui.maxInputValue_lineEdit.value
            else:
                kwargs['imn'] = self._imn
                kwargs['imx'] = self._imx

            if self._ui.selectCustomAverage_checkBox.isChecked():
                kwargs['iav'] = self._ui.average_lineEdit.value
            else:
                kwargs['iav'] = self._imean


        elif self._ui.standarization_radioButton.isChecked():
            scalingMethod = "std"
            if self._ui.selectCustomAverage_checkBox.isChecked():
                kwargs['iav'] = self._ui.average_lineEdit.value
                kwargs['isd'] = self._ui.stdDevValue_lineEdit.value
            else:
                kwargs['iav'] = self._imean
                kwargs['isd'] = self._istd

        if self._ui.keepDataTypes_radioButton.isChecked():
            print("keep type")
            keepType = True
            normalizeOutput = True
            if self._ui.selectOuptutRange_checkBox.isChecked():
                kwargs['omn'] = self._ui.minOutputValue_lineEdit.value
                kwargs['omx'] = self._ui.maxOutputValue_lineEdit.value
                if kwargs['omx'] == kwargs['omn']: return
            else:
                kwargs['omn'] = self._rmn
                kwargs['omx'] = self._rmx

        elif self._ui.keepRange_radioButton.isChecked():
            keepType = True
            normalizeOutput = True
            kwargs['omn'] = self._imn
            kwargs['omx'] = self._imx

        elif self._ui.convertToReal_radioButton.isChecked():
            keepType = False
            normalizeOutput = False
            if self._ui.selectOuptutRange_checkBox.isChecked():
                normalizeOutput = True
                kwargs['omn'] = self._ui.minOutputValue_lineEdit.value
                kwargs['omx'] = self._ui.maxOutputValue_lineEdit.value

                if kwargs['omx'] == kwargs['omn']: return

        print(scalingMethod, " keepType ", keepType, " normalizeOutput ", normalizeOutput)
        print(kwargs)

        self._viewer.cbLoopThread.requestCB(
            self._viewer, self._initialImg, scalingMethod=scalingMethod,
            keepType=keepType, normalizeOutput=normalizeOutput,
            **kwargs)

    @staticmethod
    def _scaling(editor, img,
                 scalingMethod="norm",
                 normalizeOutput=True,
                 keepType=True,
                 **kwargs):

        if scalingMethod == "reset":
            editor.img = img
            return
        elif scalingMethod == "norm":
            imn = kwargs['imn']
            imx = kwargs['imx']

            fc = 1.0 / (imx - imn)
            ds = imn
            mn = 0.0
            mx = 1.0


        elif scalingMethod == "mnorm":
            imn = kwargs['imn']
            imx = kwargs['imx']
            iav = kwargs['iav']

            fc = 1.0 / (imx - imn)
            ds = iav
            # !todo: en este caso
            mn = -1.0  # (imn -  iav) * fc
            mx = 1.0  # (imx -  iav) * fc

        elif scalingMethod == "std":
            iav = kwargs['iav']
            isd = kwargs['isd']

            fc = 1.0 / isd
            ds = iav
            mn = -3.0  # 3 desviaciones tipicas el 99% de los datos
            mx = 3.0  # 3 desviaciones tipicas el 99% de los datos

        if normalizeOutput:
            ds += mn / fc
            fc = fc / (mx - mn)

        imout = np.clip(fc * img - (fc * ds), mn, mx)
        print(imout.max())
        print(imout.min())

        if normalizeOutput:
            omn = kwargs['omn']
            omx = kwargs['omx']

            fc = omx - omn
            ds = omn
            imout = fc * imout + ds
            print(imout.max())
            print(imout.min())

        if keepType:
            imout = imout.astype(img.dtype)

        editor.img = imout
