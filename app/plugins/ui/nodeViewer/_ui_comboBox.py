# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comboBox.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_comboBox_widget(object):
    def setupUi(self, comboBox_widget):
        comboBox_widget.setObjectName("comboBox_widget")
        comboBox_widget.resize(353, 38)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(comboBox_widget.sizePolicy().hasHeightForWidth())
        comboBox_widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(comboBox_widget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(comboBox_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(comboBox_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)

        self.retranslateUi(comboBox_widget)

    #        todo
    #        QtCore.QMetaObject.connectSlotsByName(comboBox_widget)

    def retranslateUi(self, comboBox_widget):
        _translate = QtCore.QCoreApplication.translate
        comboBox_widget.setWindowTitle(_translate("comboBox_widget", "Form"))
        self.label.setText(_translate("comboBox_widget", "TextLabel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    comboBox_widget = QtWidgets.QWidget()
    ui = Ui_comboBox_widget()
    ui.setupUi(comboBox_widget)
    comboBox_widget.show()
    sys.exit(app.exec_())
