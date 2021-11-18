# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/isabel/projects/qttool/app/plugins/ui/ROIDrawer/roiviewer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ROIviewer(object):
    def setupUi(self, ROIviewer):
        ROIviewer.setObjectName("ROIviewer")
        ROIviewer.resize(514, 438)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ROIviewer.sizePolicy().hasHeightForWidth())
        ROIviewer.setSizePolicy(sizePolicy)
        self.gridLayoutWidget = QtWidgets.QWidget(ROIviewer)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.ROIgl = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.ROIgl.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.ROIgl.setContentsMargins(0, 0, 0, 0)
        self.ROIgl.setObjectName("ROIgl")

        self.retranslateUi(ROIviewer)
        QtCore.QMetaObject.connectSlotsByName(ROIviewer)

    def retranslateUi(self, ROIviewer):
        _translate = QtCore.QCoreApplication.translate
        ROIviewer.setWindowTitle(_translate("ROIviewer", "ROI Viewer"))
