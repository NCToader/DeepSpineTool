# -*- coding: utf-8 -*-

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
