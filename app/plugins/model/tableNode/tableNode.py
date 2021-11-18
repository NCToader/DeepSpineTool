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
