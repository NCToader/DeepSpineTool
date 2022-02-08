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
