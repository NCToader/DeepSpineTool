# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lineEdit.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_lineEdit_widget(object):
    def setupUi(self, lineEdit_widget):
        lineEdit_widget.setObjectName("lineEdit_widget")
        lineEdit_widget.resize(340, 38)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lineEdit_widget.sizePolicy().hasHeightForWidth())
        lineEdit_widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(lineEdit_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.attr_label = QtWidgets.QLabel(lineEdit_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attr_label.sizePolicy().hasHeightForWidth())
        self.attr_label.setSizePolicy(sizePolicy)
        self.attr_label.setObjectName("attr_label")
        self.horizontalLayout.addWidget(self.attr_label)
        self.lineEdit = QtWidgets.QLineEdit(lineEdit_widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.retranslateUi(lineEdit_widget)

    #        !todo:Qt error. 
    #        QtCore.QMetaObject.connectSlotsByName(lineEdit_widget)

    def retranslateUi(self, lineEdit_widget):
        _translate = QtCore.QCoreApplication.translate
        lineEdit_widget.setWindowTitle(_translate("lineEdit_widget", "Form"))
        self.attr_label.setText(_translate("lineEdit_widget", "TextLabel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    lineEdit_widget = QtWidgets.QWidget()
    ui = Ui_lineEdit_widget()
    ui.setupUi(lineEdit_widget)
    lineEdit_widget.show()
    sys.exit(app.exec_())
