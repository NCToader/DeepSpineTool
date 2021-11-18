# -*- coding: utf-8 -*-
"""
Created on Mon Dic  1 16:21:50 2019

@author: Marcos
"""
from PyQt5 import Qt
import traceback

from app.core.ui import CBThread, ICBThread
from app.core.utils import StdoutManager

from app.core.ui.outProcessigDialogStream import OutProcessigDialogStream
from app.core.ui.ui_Processing import Ui_processing_dialog
from app.core.ui import _icons

from app.core.ui import mainWindow as mw  # !todo:eliminar la referencia cruzada


class ProcessingDialog(Qt.QDialog):
    terminateSignal = Qt.pyqtSignal()

    def __init__(self, parent=None,
                 title=None,
                 finishMsg=None,
                 terminateMsg=None,
                 closeOnFinished=True,
                 closeButtonEnabled=False,
                 iconNum=1):

        super().__init__(parent)
        self._ui = Ui_processing_dialog()
        self._ui.setupUi(self)

        if title is not None:
            self._ui.processing_label.setText(title)

        self._ui.movie = Qt.QMovie(":/icons/" + str(iconNum))
        self._ui.img_label.setMovie(self._ui.movie)
        self._ui.movie.setScaledSize(Qt.QSize(200, 200))

        self.setFixedSize(self.sizeHint())
        self.layout().setSizeConstraint(Qt.QLayout.SetFixedSize)

        self._finished = False
        self._finishedWithError = False
        self._terminateSignalSend = False

        self.finishMsg = finishMsg
        self.terminateMsg = terminateMsg
        self.closeButtonEnabled = closeButtonEnabled
        self.closeOnFinished = closeOnFinished
        self._ui.close_checkBox.setChecked(closeOnFinished)

        self.setWindowFlags(
            Qt.Qt.Window | Qt.Qt.WindowTitleHint | Qt.Qt.CustomizeWindowHint)

        self._ui.hideConsole_toolButton.toggled.connect(self._changeArrow)
        self._ui.close_checkBox.stateChanged.connect(self._cof)
        self._ui.close_pushButton.clicked.connect(self._close)

    @Qt.pyqtSlot()
    def finish(self):
        if self._finished: return
        self._finished = True
        self._finishedWithError = False
        self._ui.close_pushButton.setEnabled(True)
        self._ui.movie.stop()
        self._ui.progressBar.setValue(100)
        self.addTextToConsole(self.finishMsg, color=Qt.QColor(0, 128, 0))
        if self._closeOnFinished:
            #            self.done(Qt.QDialog.Accepted)
            self.accept()

    @Qt.pyqtSlot(str)
    def finishWithError(self, value):
        if self._finished: return
        self._finished = True
        self._finishedWithError = True
        self._ui.close_pushButton.setEnabled(True)
        self._ui.movie.stop()
        self.addTextToConsole(value, color=Qt.QColor(128, 0, 0))
        if self._closeOnFinished:
            #            self.done(Qt.QDialog.Rejected)
            self.reject()

    @Qt.pyqtSlot(int)
    def _cof(self, state):
        self._closeOnFinished = state != 0

    @Qt.pyqtSlot()
    def _close(self):
        if self._finished:
            if self._finishedWithError:
                #                self.done(Qt.QDialog.Rejected)
                self.reject()
            else:
                #                self.done(Qt.QDialog.Accepted)
                self.accept()
        else:
            if not self._terminateSignalSend:

                if mw.MainWindow().confirmMsg(
                        "Are you sure you want to cancel the current process?"):
                    self.closeOnFinished = True
                    self._ui.close_checkBox.setEnabled(False)
                    self._terminateSignalSend = True
                    self.terminateSignal.emit()

    @Qt.pyqtSlot(bool)
    def _changeArrow(self, show):
        sender = self.sender()
        if show:
            sender.setArrowType(Qt.Qt.UpArrow)
        else:
            sender.setArrowType(Qt.Qt.DownArrow)

    @property
    def closeButtonEnabled(self):
        self._ui.close_pushButton.isEnabled()

    @closeButtonEnabled.setter
    def closeButtonEnabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean value expected")
        if not self._finished:
            self._ui.close_pushButton.setEnabled(value)

    @property
    def closeOnFinished(self):
        self._ui.close_pushButton.isEnabled()

    @closeOnFinished.setter
    def closeOnFinished(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean value expected")

        self._closeOnFinished = value
        self._ui.close_checkBox.setChecked(value)

    @property
    def finishMsg(self):
        return self._finishMsg

    @finishMsg.setter
    def finishMsg(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("String value expected:")
        self._finishMsg = "" if value is None else value

    @property
    def terminateMsg(self):
        return self._terminateMsg

    @terminateMsg.setter
    def terminateMsg(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("String value expected")

        self._terminateMsg = value

    @property
    def editor(self):
        return self._ui.console_textEdit

    @property
    def hideProgressBar(self):
        return self._ui.progressBar_widget.isHidden()

    @hideProgressBar.setter
    def hideProgressBar(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean value expected")

        if value:
            self._ui.progressBar_widget.hide()
        else:
            self._ui.progressBar_widget.show()

    @property
    def hideConsole(self):
        return self._ui.console_widget.isHidden()

    @hideConsole.setter
    def hideConsole(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean value expected")

        if value:
            self._ui.console_widget.hide()
        else:
            self._ui.console_widget.show()

    @Qt.pyqtSlot(str, Qt.QColor)
    def addTextToConsole(self, text, color=None):
        # !todo: comprobación de tipos
        self._ui.console_textEdit.moveCursor(Qt.QTextCursor.End)

        if color:
            tc = self._ui.console_textEdit.textColor()
            self._ui.console_textEdit.setTextColor(color)

        self._ui.console_textEdit.insertPlainText(text)

        if color:
            self._ui.console_textEdit.setTextColor(tc)

    def show(self):
        self._ui.movie.start()
        super().show()

    def exec(self):
        self._ui.movie.start()
        return super().exec()

    def __initExecCB(self, redirectOutput):
        self._finished = False
        self._terminateSignalSend = False
        self._finishedWithError = False

        if redirectOutput:
            stdout = OutProcessigDialogStream(self,
                                              out=StdoutManager().defaultstdout)
            stderr = OutProcessigDialogStream(self,
                                              out=StdoutManager().defaultstderr,
                                              color=Qt.QColor(255, 0, 0))
            StdoutManager().pushStdout(stdout)
            StdoutManager().pushStderr(stderr)

    def __finalizeExecCB(self, redirectOutput):
        if redirectOutput:
            StdoutManager().popStdout()
            StdoutManager().popStderr()

    def execCB(self, cb, redirectOutput=True):
        self.__initExecCB(redirectOutput)
        self._ui.close_checkBox.setEnabled(True)
        self.closeButtonEnabled = False
        self.hideProgressBar = True
        result = Qt.QDialog.Rejected

        try:
            t = CBThread(cb)
            t.finishSignal.connect(self.finish)
            t.errorSignal.connect(self.finishWithError)
            #            self.terminateSignal.connect(t.stop)
            t.start()
            # todo: no funciona el return
            result = self.exec()
            result = Qt.QDialog.Rejected if self._finishedWithError else \
                Qt.QDialog.Accepted

            print(self._finishedWithError, self._finished)

        except Exception:
            traceback.print_exc()

        self.__finalizeExecCB(redirectOutput)
        return result

    def execICB(self, cb, redirectOutput=True):
        self.__initExecCB(redirectOutput)
        result = Qt.QDialog.Rejected
        self._ui.close_checkBox.setEnabled(True)

        try:
            t = ICBThread(cb)
            t.finishSignal.connect(self.finish)
            t.errorSignal.connect(self.finishWithError)
            self.terminateSignal.connect(t.sendTerminateRequest)
            t.progressSignal.connect(self._ui.progressBar.setValue)
            t.start()
            # todo: no funciona el return
            result = self.exec()
            result = Qt.QDialog.Rejected if self._finishedWithError else \
                Qt.QDialog.Accepted
            print(self._finishedWithError, self._finished)

        except Exception:
            traceback.print_exc()

        self.__finalizeExecCB(redirectOutput)
        return result


if __name__ == '__main__':

    import sys
    import time

    app = Qt.QApplication(sys.argv)

    ex = ProcessingDialog(title="Testing ...")
    ex.closeButtonEnabled = True
    ex.closeOnFinished = False
    ex.hideConsole = False
    ex.hideProgressBar = False
    ex.finishMsg = \
        """
        #################################
        ## Finalizado
        #################################
        """
    ex.terminateMsg = \
        """
        #################################
        ## Terminate
        #################################
        """


    def test():
        for i in range(10):
            yield i * 10
            print(i)
            time.sleep(1)


    ex.execICB(test)
