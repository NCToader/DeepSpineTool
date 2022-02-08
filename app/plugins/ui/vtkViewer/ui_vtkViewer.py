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
