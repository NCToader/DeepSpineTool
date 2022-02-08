# -*- coding: utf-8 -*-

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

# Form implementation generated from reading ui file 'SceneManagerTree.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SceneManager(object):
    def setupUi(self, Form_SceneManager):
        Form_SceneManager.setObjectName("Form_SceneManager")
        Form_SceneManager.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form_SceneManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(Form_SceneManager)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.headerItem().setText(1, "2")
        self.verticalLayout.addWidget(self.treeWidget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_ShowType = QtWidgets.QCheckBox(Form_SceneManager)
        self.checkBox_ShowType.setObjectName("checkBox_ShowType")
        self.gridLayout.addWidget(self.checkBox_ShowType, 3, 0, 1, 1)
        self.pushButton_AddNode = QtWidgets.QPushButton(Form_SceneManager)
        self.pushButton_AddNode.setObjectName("pushButton_AddNode")
        self.gridLayout.addWidget(self.pushButton_AddNode, 1, 0, 1, 1)
        self.pushButton_RemoveNode = QtWidgets.QPushButton(Form_SceneManager)
        self.pushButton_RemoveNode.setObjectName("pushButton_RemoveNode")
        self.gridLayout.addWidget(self.pushButton_RemoveNode, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form_SceneManager)
        QtCore.QMetaObject.connectSlotsByName(Form_SceneManager)

    def retranslateUi(self, Form_SceneManager):
        _translate = QtCore.QCoreApplication.translate
        Form_SceneManager.setWindowTitle(_translate("Form_SceneManager", "Form"))
        self.checkBox_ShowType.setText(_translate("Form_SceneManager", "Show Type"))
        self.pushButton_AddNode.setText(_translate("Form_SceneManager", "Add Node"))
        self.pushButton_RemoveNode.setText(_translate("Form_SceneManager", "Remove Selected Nodes"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_SceneManager = QtWidgets.QWidget()
    ui = Ui_Form_SceneManager()
    ui.setupUi(Form_SceneManager)
    Form_SceneManager.show()
    sys.exit(app.exec_())
