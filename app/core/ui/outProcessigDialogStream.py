# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 18:34:14 2019

@author: URJC
https://stackoverflow.com/questions/17132994/pyside-and-python-logging
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
from app.core.utils import OutStreamBase


# , StdoutManager, OutStrStream


class _OPDSMeta(type(Qt.QObject), type(OutStreamBase)):
    pass


class OutProcessigDialogStream(OutStreamBase, Qt.QObject, metaclass=_OPDSMeta):
    printSignal = Qt.pyqtSignal(str, Qt.QColor)

    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        super(Qt.QObject, self).__init__()

        self._edit = edit
        self._out = out
        self._color = edit.editor.textColor() if color is None else color
        self.printSignal.connect(edit.addTextToConsole)

    def write(self, m):
        self.printSignal.emit(m, self._color)

        if self._out:
            self._out.write(m)

    def flush(self):
        if self._out:
            self._out.flush()
