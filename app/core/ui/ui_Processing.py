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

# Form implementation generated from reading ui file '000processing.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_processing_dialog(object):
    def setupUi(self, processing_dialog):
        processing_dialog.setObjectName("processing_dialog")
        processing_dialog.resize(684, 392)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(processing_dialog.sizePolicy().hasHeightForWidth())
        processing_dialog.setSizePolicy(sizePolicy)
        processing_dialog.setMinimumSize(QtCore.QSize(400, 0))
        processing_dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(processing_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.processing_label = QtWidgets.QLabel(processing_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processing_label.sizePolicy().hasHeightForWidth())
        self.processing_label.setSizePolicy(sizePolicy)
        self.processing_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.processing_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.processing_label.setLineWidth(1)
        self.processing_label.setTextFormat(QtCore.Qt.RichText)
        self.processing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.processing_label.setObjectName("processing_label")
        self.verticalLayout.addWidget(self.processing_label)
        self.img_widget = QtWidgets.QWidget(processing_dialog)
        self.img_widget.setObjectName("img_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.img_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.imgNclose_widget = QtWidgets.QWidget(self.img_widget)
        self.imgNclose_widget.setObjectName("imgNclose_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.imgNclose_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.img_label = QtWidgets.QLabel(self.imgNclose_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_label.sizePolicy().hasHeightForWidth())
        self.img_label.setSizePolicy(sizePolicy)
        self.img_label.setStyleSheet("background-color:rgb(255,255,255)")
        self.img_label.setText("")
        self.img_label.setObjectName("img_label")
        self.horizontalLayout.addWidget(self.img_label)
        self.close_widget = QtWidgets.QWidget(self.imgNclose_widget)
        self.close_widget.setObjectName("close_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.close_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.close_pushButton = QtWidgets.QPushButton(self.close_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_pushButton.sizePolicy().hasHeightForWidth())
        self.close_pushButton.setSizePolicy(sizePolicy)
        self.close_pushButton.setObjectName("close_pushButton")
        self.verticalLayout_4.addWidget(self.close_pushButton)
        self.close_checkBox = QtWidgets.QCheckBox(self.close_widget)
        self.close_checkBox.setChecked(True)
        self.close_checkBox.setObjectName("close_checkBox")
        self.verticalLayout_4.addWidget(self.close_checkBox)
        self.horizontalLayout.addWidget(self.close_widget)
        self.verticalLayout_2.addWidget(self.imgNclose_widget)
        self.verticalLayout.addWidget(self.img_widget)
        self.console_widget = QtWidgets.QWidget(processing_dialog)
        self.console_widget.setObjectName("console_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.console_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressBar_widget = QtWidgets.QWidget(self.console_widget)
        self.progressBar_widget.setObjectName("progressBar_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.progressBar_widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.progressBar = QtWidgets.QProgressBar(self.progressBar_widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_5.addWidget(self.progressBar)
        self.verticalLayout_3.addWidget(self.progressBar_widget)
        self.hideConsole_toolButton = QtWidgets.QToolButton(self.console_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideConsole_toolButton.sizePolicy().hasHeightForWidth())
        self.hideConsole_toolButton.setSizePolicy(sizePolicy)
        self.hideConsole_toolButton.setIconSize(QtCore.QSize(6, 6))
        self.hideConsole_toolButton.setCheckable(True)
        self.hideConsole_toolButton.setChecked(False)
        self.hideConsole_toolButton.setArrowType(QtCore.Qt.DownArrow)
        self.hideConsole_toolButton.setObjectName("hideConsole_toolButton")
        self.verticalLayout_3.addWidget(self.hideConsole_toolButton)
        self.console_textEdit = QtWidgets.QTextEdit(self.console_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_textEdit.sizePolicy().hasHeightForWidth())
        self.console_textEdit.setSizePolicy(sizePolicy)
        self.console_textEdit.setUndoRedoEnabled(False)
        self.console_textEdit.setReadOnly(True)
        self.console_textEdit.setObjectName("console_textEdit")
        self.verticalLayout_3.addWidget(self.console_textEdit)
        self.verticalLayout.addWidget(self.console_widget)
        self.widget = QtWidgets.QWidget(processing_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(processing_dialog)
        self.hideConsole_toolButton.toggled['bool'].connect(self.console_textEdit.setHidden)

    # !todo: no se porque esto no funciona!!!!
    #        QtCore.QMetaObject.connectSlotsByName(processing_dialog)

    def retranslateUi(self, processing_dialog):
        _translate = QtCore.QCoreApplication.translate
        processing_dialog.setWindowTitle(_translate("processing_dialog", "Procesing"))
        self.processing_label.setText(_translate("processing_dialog",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Processing ....</span></p></body></html>"))
        self.close_pushButton.setText(_translate("processing_dialog", "Close"))
        self.close_checkBox.setText(_translate("processing_dialog", "Close when finished"))
        self.console_textEdit.setHtml(_translate("processing_dialog",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


import app.core.ui._icons

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    processing_dialog = QtWidgets.QDialog()
    ui = Ui_processing_dialog()
    ui.setupUi(processing_dialog)
    processing_dialog.show()
    sys.exit(app.exec_())
