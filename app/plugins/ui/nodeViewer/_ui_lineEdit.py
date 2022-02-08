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
