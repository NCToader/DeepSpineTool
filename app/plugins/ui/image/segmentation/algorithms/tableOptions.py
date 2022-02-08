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
from app.core.ui import mainWindow as MW
import numpy as np

class TableOptions(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("contrastBrightnessEditor_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)
            self.to_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=parent)
            vLayout = Qt.QVBoxLayout()
            self.connectedCB = Qt.QCheckBox('Check sp-dendr connections')
            self.recalculateButton = Qt.QPushButton('Update table')
            self.diagonalsButton = Qt.QCheckBox('Diagonals count as same element')
            self.diagonalsButton.setChecked(False)
            vLayout.addWidget(self.connectedCB)
            vLayout.addWidget(self.diagonalsButton)
            self.to_layout.addLayout(vLayout)
            self.to_layout.addWidget(self.recalculateButton)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = TableOptions._UI(parent=self)
        self._viewer = viewer
        self._ui.recalculateButton.clicked.connect(self.recalculateTable)
        self._ui.connectedCB.stateChanged.connect(self.cbRecalculateState)
        self._ui.diagonalsButton.stateChanged.connect(self.cbDiagonalsState)


    def recalculateTable(self):
        self._viewer.updateLabels()

    def cbDiagonalsState(self, state):
        if state > 0:
            self._viewer.diagonalsConnected = True
        else:
            self._viewer.diagonalsConnected = False

    def cbRecalculateState(self, state):
        if state > 0:
            self._viewer.checkConnectedToDendrite = True
        else:
            self._viewer.checkConnectedToDendrite = False
