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

from app.core.ui.mainWindow import MainWindow
from app.plugins.ui.saverManager import Saver
from app.core.ui import mainWindow as MW
from app.plugins.ui.sceneManagerUi import sceneManager as scm
from app.plugins.model.tableNode.tableNode import TableNode
import os
import sys, csv

class TableSaver(Saver):
    def __init__(self, *args):
        self._menuPath = ["Table"]
        self._name = 'Save csv'
        super().__init__(*args)

    @classmethod
    def _cb(clss):
        mw = MW.MainWindow()
        smUI = scm.SceneManagerUI()
        nodes = [n for n in smUI.selectedNodes if isinstance(n, TableNode)]
        if len(nodes) == 0:
            mw.warningMsg("No tables selected")
        elif len(nodes) == 1:
            fn = mw.saveFileDialog(filters=['CSV (*.csv)', 'All files(*)'])
            if fn[0]:
                table = nodes[0]
                with open(os.path.join(fn[0]), 'w') as stream:
                    writer = csv.writer(stream)
                    headerRow=[]
                    for c in range(table.tableWidget.columnCount()):
                        it = table.tableWidget.horizontalHeaderItem(c)
                        headerRow.append(str(c+1) if it is None else it.text())
                    writer.writerow(headerRow)
                    for row in range(table.tableWidget.rowCount()):
                        rowData = []
                        for column in range(table.tableWidget.columnCount()):
                            item = table.tableWidget.item(row, column)
                            if item is not None:
                                rowData.append(item.text())
                            else:
                                rowData.append('')
                        writer.writerow(rowData)

