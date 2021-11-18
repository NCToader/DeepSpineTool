# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodeViewer.v3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_nodeViewer_form(object):
    def setupUi(self, nodeViewer_form):
        nodeViewer_form.setObjectName("nodeViewer_form")
        nodeViewer_form.resize(162, 655)
        self.verticalLayout = QtWidgets.QVBoxLayout(nodeViewer_form)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgets_layout = QtWidgets.QVBoxLayout()
        self.widgets_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.widgets_layout.setObjectName("widgets_layout")
        self.nodeType_layout = QtWidgets.QHBoxLayout()
        self.nodeType_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.nodeType_layout.setObjectName("nodeType_layout")
        self.label = QtWidgets.QLabel(nodeViewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.nodeType_layout.addWidget(self.label)
        self.nodeType_lineEdit = QtWidgets.QLineEdit(nodeViewer_form)
        self.nodeType_lineEdit.setEnabled(True)
        self.nodeType_lineEdit.setText("")
        self.nodeType_lineEdit.setFrame(True)
        self.nodeType_lineEdit.setReadOnly(True)
        self.nodeType_lineEdit.setObjectName("nodeType_lineEdit")
        self.nodeType_layout.addWidget(self.nodeType_lineEdit)
        self.widgets_layout.addLayout(self.nodeType_layout)
        self.localTransform_layout = QtWidgets.QHBoxLayout()
        self.localTransform_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.localTransform_layout.setObjectName("localTransform_layout")
        self.label_3 = QtWidgets.QLabel(nodeViewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.localTransform_layout.addWidget(self.label_3)
        self.localTransform_widget = QtWidgets.QWidget(nodeViewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localTransform_widget.sizePolicy().hasHeightForWidth())
        self.localTransform_widget.setSizePolicy(sizePolicy)
        self.localTransform_widget.setObjectName("localTransform_widget")
        self.localTransform_layout.addWidget(self.localTransform_widget)
        self.widgets_layout.addLayout(self.localTransform_layout)
        self.globalTransform_layout = QtWidgets.QHBoxLayout()
        self.globalTransform_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.globalTransform_layout.setObjectName("globalTransform_layout")
        self.label_4 = QtWidgets.QLabel(nodeViewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.globalTransform_layout.addWidget(self.label_4)
        self.globalTransform_widget = QtWidgets.QWidget(nodeViewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalTransform_widget.sizePolicy().hasHeightForWidth())
        self.globalTransform_widget.setSizePolicy(sizePolicy)
        self.globalTransform_widget.setObjectName("globalTransform_widget")
        self.globalTransform_layout.addWidget(self.globalTransform_widget)
        self.widgets_layout.addLayout(self.globalTransform_layout)
        self.verticalLayout.addLayout(self.widgets_layout)
        self.freeSpace_layout = QtWidgets.QHBoxLayout()
        self.freeSpace_layout.setObjectName("freeSpace_layout")
        self.widget = QtWidgets.QWidget(nodeViewer_form)
        self.widget.setObjectName("widget")
        self.freeSpace_layout.addWidget(self.widget)
        self.verticalLayout.addLayout(self.freeSpace_layout)

        self.retranslateUi(nodeViewer_form)
        QtCore.QMetaObject.connectSlotsByName(nodeViewer_form)

    def retranslateUi(self, nodeViewer_form):
        _translate = QtCore.QCoreApplication.translate
        nodeViewer_form.setWindowTitle(_translate("nodeViewer_form", "Form"))
        self.label.setText(_translate("nodeViewer_form", "Node Type:"))
        self.label_3.setText(_translate("nodeViewer_form", "Local Transform: "))
        self.label_4.setText(_translate("nodeViewer_form", "Global Transform:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    nodeViewer_form = QtWidgets.QWidget()
    ui = Ui_nodeViewer_form()
    ui.setupUi(nodeViewer_form)
    nodeViewer_form.show()
    sys.exit(app.exec_())
