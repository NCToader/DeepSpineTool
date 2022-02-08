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

from app.core.model.sceneNode import SceneNode
from app.core.ui import mainWindow as MW
from PyQt5 import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import Qt, QtWidgets, QtCore

class TableNode(SceneNode):
    def __init__(self, name=None, spinesDict = None):
        super().__init__(name)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Volume', 'Area'])
        self.tableWidget.setRowCount(len(spinesDict))
        self.fillTable(spinesDict)

    def fillTable(self, spinesDict):
        for row in range(len(spinesDict)):
            id_item = QTableWidgetItem(str(row + 1))
            self.tableWidget.setItem(row, 0, QTableWidgetItem(id_item))
            volume = QTableWidgetItem(str(spinesDict[row]['volume']))
            self.tableWidget.setItem(row, 1, volume)
            area = QTableWidgetItem(str(spinesDict[row]['area']))
            self.tableWidget.setItem(row, 2, area)


def init():
    tablenode = TableNode()
