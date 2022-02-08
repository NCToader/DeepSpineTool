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

class CustomDialog(Qt.QDialog):

    def  __init__(self, nodes, imageTypes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = MW.MainWindow()
        self.setWindowTitle("Choose corresponding images")
        self.nodes = np.copy(nodes)
        self.imagesNode = dict()

        form = Qt.QFormLayout(self)
        buttons = []
        lineEdits = []

        for i in range(len(nodes)):
            bt = Qt.QPushButton('Choose ' + imageTypes[i] + ' image')
            le = Qt.QLineEdit()
            buttons.append(bt)
            lineEdits.append(le)
            form.addRow(bt, le)

        for i in range(len(buttons)):
            buttons[i].clicked.connect(lambda _, i=i: self.getItem(imageTypes[i], lineEdits[i]))

        buttonBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok | Qt.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        form.addRow(buttonBox)


    def getItem(self, imageType, le):
        items = [n.name for n in self.nodes]
        dialogTitle = 'Select ' + imageType + ' image'
        item, ok = Qt.QInputDialog.getItem(self._mw, 'Select image', dialogTitle, items, 0, False)
        if ok and item:
            le.setText(item)
            self.imagesNode[imageType] = self.nodes[items.index(item)]
        else:
            self._mw.warningMsg('Nothing selected')