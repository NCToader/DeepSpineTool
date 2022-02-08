# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:55:19 2019

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
import traceback
from copy import copy
import time


class CBThread(Qt.QThread):
    finishSignal = Qt.pyqtSignal()
    errorSignal = Qt.pyqtSignal(str)

    def __init__(self, cb, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cb = cb
        self.finishSignal.connect(self.deleteLater)

    def run(self):
        try:
            self._cb()
        except Exception as e:
            traceback.print_exc()
            self.errorSignal.emit(str(e))

        self.finishSignal.emit()


class ICBThread(Qt.QThread):
    finishSignal = Qt.pyqtSignal()
    errorSignal = Qt.pyqtSignal(str)
    progressSignal = Qt.pyqtSignal(int)

    def __init__(self, icb, terminateRequestMsg=None, *args, **kwargs):
        """
        Iterative Callback Thread
        """
        super().__init__(*args, **kwargs)
        self._icb = icb
        self._mutex = Qt.QMutex()
        self._teminateRequest = False
        self._terminateRequestMsg = \
            terminateRequestMsg if terminateRequestMsg is not None else \
                """
                ################################
                # Execution not completed.  
                # Terminate request sent.
                ################################
                """

        self.finishSignal.connect(self.deleteLater)
        self.errorSignal.connect(self.deleteLater)

    @Qt.pyqtSlot()
    def sendTerminateRequest(self):
        self._mutex.lock()
        self._teminateRequest = True
        self._mutex.unlock()

    def _terminateRequested(self):
        self._mutex.lock()
        result = self._teminateRequest
        self._mutex.unlock()

        return result

    def run(self):
        try:
            terminateRequested = False
            for i in self._icb():
                if self._terminateRequested():
                    terminateRequested = True
                    break
                else:
                    if isinstance(i, int):
                        self.progressSignal.emit(i)
            if terminateRequested:
                self.errorSignal.emit(self._terminateRequestMsg)
            else:
                self.finishSignal.emit()

        except Exception as e:
            traceback.print_exc()
            self.errorSignal.emit(str(e))


class CBLoopThread(Qt.QThread):

    def __init__(self, *args, **kwargs):
        """
        Callback Loop Thread
        """
        super().__init__(*args, **kwargs)
        self._dataMutex = Qt.QMutex()
        self._runMutex = Qt.QMutex()
        self._wakeup = Qt.QWaitCondition()

        self._cb = None
        self._args = None

        self._isRunning = False
        self._terminateRequest = False
        self._cbRequest = False
        self._exe = False

    def waitForCB(self):
        if not self.isLoopRunning: return
        while self.isCBRunning or self.cbRequested:
            time.sleep(0.1)

    def unlock(self):
        self._dataMutex.unlock()

    @property
    def isLoopRunning(self):
        Qt.QMutexLocker(self._dataMutex)
        return self._isRunning

    @property
    def isCBRunning(self):
        Qt.QMutexLocker(self._dataMutex)
        return self._exe

    @property
    def cbRequested(self):
        Qt.QMutexLocker(self._dataMutex)
        return self._cbRequest

    def terminate(self):
        '''Blocking'''
        self._dataMutex.lock()
        self._terminateRequest = True
        self._dataMutex.unlock()

        while (self.isLoopRunning):
            self._dataMutex.unlock()
            self._wakeup.wakeAll()
            time.sleep(0.2)
            self._dataMutex.lock()

        self._dataMutex.unlock()

    def requestCB(self, *args, **kwargs):
        Qt.QMutexLocker(self._dataMutex)
        self._args = (args, kwargs)
        self._cbRequest = True
        self._wakeup.wakeAll()

    def setCallback(self, cb=None):
        Qt.QMutexLocker(self._dataMutex)
        self._cb = cb
        self._cbRequest = False

    def run(self):
        self._dataMutex.lock()
        self._isRunning = True
        self._exe = False
        cbr = self._cbRequest

        while not self._terminateRequest:
            cb = self._cb
            args = None if self._args is None else self._args[0]
            kwargs = None if self._args is None else self._args[1]
            self._cbRequest = False
            if cb is not None and cbr:
                self._exe = True
            self._dataMutex.unlock()

            if cb is not None and cbr:
                cb(*args, **kwargs)

            self._dataMutex.lock()
            self._exe = False

            cbr = self._cbRequest
            if not cbr:
                self._dataMutex.unlock()

                # todo: Si en este momento hay un request, se perdería
                self._runMutex.lock()
                self._wakeup.wait(self._runMutex)
                self._runMutex.unlock()

                self._dataMutex.lock()
                cbr = self._cbRequest

        self._dataMutex.lock()
        self._isRunning = False
        self._terminateRequest = False
        self._cbRequest = False
        self._dataMutex.unlock()
