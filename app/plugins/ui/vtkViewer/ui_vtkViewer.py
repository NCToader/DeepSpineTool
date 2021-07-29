# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/isabel/projects/qttool/app/plugins/ui/vtkViewer/vtkviewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VTKViewer(object):
    def setupUi(self, VTKViewer):
        VTKViewer.setObjectName("VTKViewer")
        VTKViewer.resize(400, 300)
        VTKViewer.setMinimumSize(QtCore.QSize(0, 0))
        self.frame = QtWidgets.QFrame(VTKViewer)
        self.frame.setGeometry(QtCore.QRect(-11, -1, 421, 311))
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.retranslateUi(VTKViewer)
        QtCore.QMetaObject.connectSlotsByName(VTKViewer)

    def retranslateUi(self, VTKViewer):
        _translate = QtCore.QCoreApplication.translate
        VTKViewer.setWindowTitle(_translate("VTKViewer", "VTK Viewer"))
