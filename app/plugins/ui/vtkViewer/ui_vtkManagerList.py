# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/isabel/projects/qttool/app/plugins/ui/vtkViewer/VTKManager.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_VTKManager(object):
    def setupUi(self, Form_VTKManager):
        Form_VTKManager.setObjectName("Form_VTKManager")
        Form_VTKManager.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form_VTKManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.availableNList = QtWidgets.QListWidget(Form_VTKManager)
        self.availableNList.setObjectName("availableNList")
        self.gridLayout.addWidget(self.availableNList, 1, 0, 1, 1)
        self.pushButton_ImportNode = QtWidgets.QPushButton(Form_VTKManager)
        self.pushButton_ImportNode.setObjectName("pushButton_ImportNode")
        self.gridLayout.addWidget(self.pushButton_ImportNode, 2, 0, 1, 2)
        self.activeNList = QtWidgets.QListWidget(Form_VTKManager)
        self.activeNList.setObjectName("activeNList")
        self.gridLayout.addWidget(self.activeNList, 1, 1, 1, 1)
        self.pushButton_RemoveNode = QtWidgets.QPushButton(Form_VTKManager)
        self.pushButton_RemoveNode.setObjectName("pushButton_RemoveNode")
        self.gridLayout.addWidget(self.pushButton_RemoveNode, 3, 0, 1, 2)
        self.activeNLabel = QtWidgets.QLabel(Form_VTKManager)
        self.activeNLabel.setObjectName("activeNLabel")
        self.gridLayout.addWidget(self.activeNLabel, 0, 1, 1, 1)
        self.availableNLabel = QtWidgets.QLabel(Form_VTKManager)
        self.availableNLabel.setObjectName("availableNLabel")
        self.gridLayout.addWidget(self.availableNLabel, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form_VTKManager)
        QtCore.QMetaObject.connectSlotsByName(Form_VTKManager)

    def retranslateUi(self, Form_VTKManager):
        _translate = QtCore.QCoreApplication.translate
        Form_VTKManager.setWindowTitle(_translate("Form_VTKManager", "Form"))
        self.pushButton_ImportNode.setText(_translate("Form_VTKManager", "Add node(s)"))
        self.pushButton_RemoveNode.setText(_translate("Form_VTKManager", "Remove node(s)"))
        self.activeNLabel.setText(_translate("Form_VTKManager", "Active nodes"))
        self.availableNLabel.setText(_translate("Form_VTKManager", "Available nodes"))
