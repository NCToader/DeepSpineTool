# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Image3Toolbar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_image3Toolbar_widget(object):
    def setupUi(self, image3Toolbar_widget):
        image3Toolbar_widget.setObjectName("image3Toolbar_widget")
        image3Toolbar_widget.setEnabled(True)
        image3Toolbar_widget.resize(584, 146)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(image3Toolbar_widget)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.vertical_widget = QtWidgets.QWidget(image3Toolbar_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vertical_widget.sizePolicy().hasHeightForWidth())
        self.vertical_widget.setSizePolicy(sizePolicy)
        self.vertical_widget.setObjectName("vertical_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.vertical_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalButtons_widget = QtWidgets.QWidget(self.vertical_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalButtons_widget.sizePolicy().hasHeightForWidth())
        self.verticalButtons_widget.setSizePolicy(sizePolicy)
        self.verticalButtons_widget.setObjectName("verticalButtons_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalButtons_widget)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalShowAll_pushButton = QtWidgets.QPushButton(self.verticalButtons_widget)
        self.verticalShowAll_pushButton.setObjectName("verticalShowAll_pushButton")
        self.verticalLayout_4.addWidget(self.verticalShowAll_pushButton)
        self.verticalZoomToData_pushButton = QtWidgets.QPushButton(self.verticalButtons_widget)
        self.verticalZoomToData_pushButton.setObjectName("verticalZoomToData_pushButton")
        self.verticalLayout_4.addWidget(self.verticalZoomToData_pushButton)
        self.verticalPlaneSelector_widget = QtWidgets.QWidget(self.verticalButtons_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalPlaneSelector_widget.sizePolicy().hasHeightForWidth())
        self.verticalPlaneSelector_widget.setSizePolicy(sizePolicy)
        self.verticalPlaneSelector_widget.setObjectName("verticalPlaneSelector_widget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.verticalPlaneSelector_widget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalPlaneXY_toolButton = QtWidgets.QToolButton(self.verticalPlaneSelector_widget)
        self.verticalPlaneXY_toolButton.setIconSize(QtCore.QSize(20, 20))
        self.verticalPlaneXY_toolButton.setCheckable(True)
        self.verticalPlaneXY_toolButton.setChecked(True)
        self.verticalPlaneXY_toolButton.setAutoExclusive(True)
        self.verticalPlaneXY_toolButton.setObjectName("verticalPlaneXY_toolButton")
        self.horizontalLayout_7.addWidget(self.verticalPlaneXY_toolButton)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalPlaneYZ_toolButton = QtWidgets.QToolButton(self.verticalPlaneSelector_widget)
        self.verticalPlaneYZ_toolButton.setCheckable(True)
        self.verticalPlaneYZ_toolButton.setAutoExclusive(True)
        self.verticalPlaneYZ_toolButton.setObjectName("verticalPlaneYZ_toolButton")
        self.horizontalLayout_7.addWidget(self.verticalPlaneYZ_toolButton)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalPlaneZX_toolButton = QtWidgets.QToolButton(self.verticalPlaneSelector_widget)
        self.verticalPlaneZX_toolButton.setCheckable(True)
        self.verticalPlaneZX_toolButton.setAutoExclusive(True)
        self.verticalPlaneZX_toolButton.setObjectName("verticalPlaneZX_toolButton")
        self.horizontalLayout_7.addWidget(self.verticalPlaneZX_toolButton)
        self.verticalLayout_4.addWidget(self.verticalPlaneSelector_widget)
        self.verticalMP_widget = QtWidgets.QWidget(self.verticalButtons_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalMP_widget.sizePolicy().hasHeightForWidth())
        self.verticalMP_widget.setSizePolicy(sizePolicy)
        self.verticalMP_widget.setObjectName("verticalMP_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.verticalMP_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalMP_checkBox = QtWidgets.QCheckBox(self.verticalMP_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalMP_checkBox.sizePolicy().hasHeightForWidth())
        self.verticalMP_checkBox.setSizePolicy(sizePolicy)
        self.verticalMP_checkBox.setText("")
        self.verticalMP_checkBox.setObjectName("verticalMP_checkBox")
        self.horizontalLayout_2.addWidget(self.verticalMP_checkBox)
        self.verticalMPLabel_widget = QtWidgets.QWidget(self.verticalMP_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalMPLabel_widget.sizePolicy().hasHeightForWidth())
        self.verticalMPLabel_widget.setSizePolicy(sizePolicy)
        self.verticalMPLabel_widget.setObjectName("verticalMPLabel_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalMPLabel_widget)
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalMP_label_1 = QtWidgets.QLabel(self.verticalMPLabel_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalMP_label_1.sizePolicy().hasHeightForWidth())
        self.verticalMP_label_1.setSizePolicy(sizePolicy)
        self.verticalMP_label_1.setObjectName("verticalMP_label_1")
        self.verticalLayout.addWidget(self.verticalMP_label_1)
        self.verticalMP_label_2 = QtWidgets.QLabel(self.verticalMPLabel_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalMP_label_2.sizePolicy().hasHeightForWidth())
        self.verticalMP_label_2.setSizePolicy(sizePolicy)
        self.verticalMP_label_2.setObjectName("verticalMP_label_2")
        self.verticalLayout.addWidget(self.verticalMP_label_2)
        self.horizontalLayout_2.addWidget(self.verticalMPLabel_widget)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_4.addWidget(self.verticalMP_widget)
        self.verticalResize_widget = QtWidgets.QWidget(self.verticalButtons_widget)
        self.verticalResize_widget.setObjectName("verticalResize_widget")
        self.verticalLayout_4.addWidget(self.verticalResize_widget)
        self.horizontalLayout_4.addWidget(self.verticalButtons_widget)
        self.verticalSlider_widget = QtWidgets.QWidget(self.vertical_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_widget.sizePolicy().hasHeightForWidth())
        self.verticalSlider_widget.setSizePolicy(sizePolicy)
        self.verticalSlider_widget.setObjectName("verticalSlider_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalSlider_widget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalZ_slider = QtWidgets.QSlider(self.verticalSlider_widget)
        self.verticalZ_slider.setOrientation(QtCore.Qt.Vertical)
        self.verticalZ_slider.setObjectName("verticalZ_slider")
        self.verticalLayout_5.addWidget(self.verticalZ_slider)
        spacerItem3 = QtWidgets.QSpacerItem(0, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem3)
        self.verticalZ_label = QtWidgets.QLabel(self.verticalSlider_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalZ_label.sizePolicy().hasHeightForWidth())
        self.verticalZ_label.setSizePolicy(sizePolicy)
        self.verticalZ_label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.verticalZ_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalZ_label.setObjectName("verticalZ_label")
        self.verticalLayout_5.addWidget(self.verticalZ_label)
        self.horizontalLayout_4.addWidget(self.verticalSlider_widget)
        self.horizontalLayout_11.addWidget(self.vertical_widget)
        self.horizontal_widget = QtWidgets.QWidget(image3Toolbar_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontal_widget.sizePolicy().hasHeightForWidth())
        self.horizontal_widget.setSizePolicy(sizePolicy)
        self.horizontal_widget.setObjectName("horizontal_widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.horizontal_widget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalSlider_widget = QtWidgets.QWidget(self.horizontal_widget)
        self.horizontalSlider_widget.setObjectName("horizontalSlider_widget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalSlider_widget)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalZ_slider = QtWidgets.QSlider(self.horizontalSlider_widget)
        self.horizontalZ_slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalZ_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalZ_slider.setTickInterval(50)
        self.horizontalZ_slider.setObjectName("horizontalZ_slider")
        self.horizontalLayout_8.addWidget(self.horizontalZ_slider)
        spacerItem4 = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.horizontalZ_label = QtWidgets.QLabel(self.horizontalSlider_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalZ_label.sizePolicy().hasHeightForWidth())
        self.horizontalZ_label.setSizePolicy(sizePolicy)
        self.horizontalZ_label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.horizontalZ_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalZ_label.setObjectName("horizontalZ_label")
        self.horizontalLayout_8.addWidget(self.horizontalZ_label)
        self.verticalLayout_6.addWidget(self.horizontalSlider_widget)
        self.horizontalButtons_widget = QtWidgets.QWidget(self.horizontal_widget)
        self.horizontalButtons_widget.setObjectName("horizontalButtons_widget")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalButtons_widget)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalShowAll_pushButton = QtWidgets.QPushButton(self.horizontalButtons_widget)
        self.horizontalShowAll_pushButton.setObjectName("horizontalShowAll_pushButton")
        self.horizontalLayout_9.addWidget(self.horizontalShowAll_pushButton)
        self.horizontalZoomToData_pushButton = QtWidgets.QPushButton(self.horizontalButtons_widget)
        self.horizontalZoomToData_pushButton.setObjectName("horizontalZoomToData_pushButton")
        self.horizontalLayout_9.addWidget(self.horizontalZoomToData_pushButton)
        self.horizontalPlaneSelector_widget = QtWidgets.QWidget(self.horizontalButtons_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalPlaneSelector_widget.sizePolicy().hasHeightForWidth())
        self.horizontalPlaneSelector_widget.setSizePolicy(sizePolicy)
        self.horizontalPlaneSelector_widget.setObjectName("horizontalPlaneSelector_widget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.horizontalPlaneSelector_widget)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem5 = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.horizontalPlaneXY_toolButton = QtWidgets.QToolButton(self.horizontalPlaneSelector_widget)
        self.horizontalPlaneXY_toolButton.setCheckable(True)
        self.horizontalPlaneXY_toolButton.setChecked(True)
        self.horizontalPlaneXY_toolButton.setAutoExclusive(True)
        self.horizontalPlaneXY_toolButton.setObjectName("horizontalPlaneXY_toolButton")
        self.horizontalLayout_10.addWidget(self.horizontalPlaneXY_toolButton)
        self.horizontalPlaneYZ_toolButton = QtWidgets.QToolButton(self.horizontalPlaneSelector_widget)
        self.horizontalPlaneYZ_toolButton.setCheckable(True)
        self.horizontalPlaneYZ_toolButton.setAutoExclusive(True)
        self.horizontalPlaneYZ_toolButton.setObjectName("horizontalPlaneYZ_toolButton")
        self.horizontalLayout_10.addWidget(self.horizontalPlaneYZ_toolButton)
        self.horizontalPlaneZX_toolButton = QtWidgets.QToolButton(self.horizontalPlaneSelector_widget)
        self.horizontalPlaneZX_toolButton.setCheckable(True)
        self.horizontalPlaneZX_toolButton.setAutoExclusive(True)
        self.horizontalPlaneZX_toolButton.setObjectName("horizontalPlaneZX_toolButton")
        self.horizontalLayout_10.addWidget(self.horizontalPlaneZX_toolButton)
        spacerItem6 = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem6)
        self.horizontalLayout_9.addWidget(self.horizontalPlaneSelector_widget)
        self.horizontalMP_widget = QtWidgets.QWidget(self.horizontalButtons_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalMP_widget.sizePolicy().hasHeightForWidth())
        self.horizontalMP_widget.setSizePolicy(sizePolicy)
        self.horizontalMP_widget.setObjectName("horizontalMP_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalMP_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalMP_checkBox = QtWidgets.QCheckBox(self.horizontalMP_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalMP_checkBox.sizePolicy().hasHeightForWidth())
        self.horizontalMP_checkBox.setSizePolicy(sizePolicy)
        self.horizontalMP_checkBox.setText("")
        self.horizontalMP_checkBox.setObjectName("horizontalMP_checkBox")
        self.horizontalLayout.addWidget(self.horizontalMP_checkBox)
        self.horizontalMP_label = QtWidgets.QLabel(self.horizontalMP_widget)
        self.horizontalMP_label.setObjectName("horizontalMP_label")
        self.horizontalLayout.addWidget(self.horizontalMP_label)
        self.horizontalLayout_9.addWidget(self.horizontalMP_widget)
        self.verticalLayout_6.addWidget(self.horizontalButtons_widget)
        self.horizontalLayout_11.addWidget(self.horizontal_widget)
        self.verticalMP_label_1.setBuddy(self.verticalMP_checkBox)
        self.verticalMP_label_2.setBuddy(self.verticalMP_checkBox)
        self.verticalZ_label.setBuddy(self.verticalZ_slider)
        self.horizontalZ_label.setBuddy(self.horizontalZ_slider)

        self.retranslateUi(image3Toolbar_widget)
        self.verticalMP_checkBox.toggled['bool'].connect(self.horizontalMP_checkBox.setChecked)
        self.horizontalMP_checkBox.toggled['bool'].connect(self.verticalMP_checkBox.setChecked)
        self.horizontalZ_slider.valueChanged['int'].connect(self.horizontalZ_label.setNum)
        self.verticalZ_slider.valueChanged['int'].connect(self.verticalZ_label.setNum)
        self.horizontalZ_slider.valueChanged['int'].connect(self.verticalZ_slider.setValue)
        self.verticalZ_slider.valueChanged['int'].connect(self.horizontalZ_slider.setValue)
        self.horizontalPlaneZX_toolButton.toggled['bool'].connect(self.verticalPlaneZX_toolButton.setChecked)
        self.verticalPlaneZX_toolButton.toggled['bool'].connect(self.horizontalPlaneZX_toolButton.setChecked)
        self.horizontalPlaneYZ_toolButton.toggled['bool'].connect(self.verticalPlaneYZ_toolButton.setChecked)
        self.verticalPlaneYZ_toolButton.toggled['bool'].connect(self.horizontalPlaneYZ_toolButton.setChecked)
        self.verticalPlaneXY_toolButton.toggled['bool'].connect(self.horizontalPlaneXY_toolButton.setChecked)
        self.horizontalPlaneXY_toolButton.toggled['bool'].connect(self.verticalPlaneXY_toolButton.setChecked)
        self.horizontalZ_slider.rangeChanged['int', 'int'].connect(self.verticalZ_slider.setRange)
        self.verticalZ_slider.rangeChanged['int', 'int'].connect(self.horizontalZ_slider.setRange)

    # !todo: error de Qt
    #        QtCore.QMetaObject.connectSlotsByName(image3Toolbar_widget)

    def retranslateUi(self, image3Toolbar_widget):
        _translate = QtCore.QCoreApplication.translate
        image3Toolbar_widget.setWindowTitle(_translate("image3Toolbar_widget", "Form"))
        self.verticalShowAll_pushButton.setText(_translate("image3Toolbar_widget", "Show all"))
        self.verticalZoomToData_pushButton.setText(_translate("image3Toolbar_widget", "Zoom to Data"))
        self.verticalPlaneXY_toolButton.setText(_translate("image3Toolbar_widget", "XY"))
        self.verticalPlaneYZ_toolButton.setText(_translate("image3Toolbar_widget", "YZ"))
        self.verticalPlaneZX_toolButton.setText(_translate("image3Toolbar_widget", "ZX"))
        self.verticalMP_label_1.setText(_translate("image3Toolbar_widget", "Maximum"))
        self.verticalMP_label_2.setText(_translate("image3Toolbar_widget", "Projection"))
        self.verticalZ_label.setText(_translate("image3Toolbar_widget", "\"  \""))
        self.horizontalZ_label.setText(_translate("image3Toolbar_widget", "\"  \""))
        self.horizontalShowAll_pushButton.setText(_translate("image3Toolbar_widget", "Show all"))
        self.horizontalZoomToData_pushButton.setText(_translate("image3Toolbar_widget", "Zoom to Data"))
        self.horizontalPlaneXY_toolButton.setText(_translate("image3Toolbar_widget", "XY"))
        self.horizontalPlaneYZ_toolButton.setText(_translate("image3Toolbar_widget", "YZ"))
        self.horizontalPlaneZX_toolButton.setText(_translate("image3Toolbar_widget", "ZX"))
        self.horizontalMP_label.setText(_translate("image3Toolbar_widget", "Maximum Projection"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    image3Toolbar_widget = QtWidgets.QWidget()
    ui = Ui_image3Toolbar_widget()
    ui.setupUi(image3Toolbar_widget)
    image3Toolbar_widget.show()
    sys.exit(app.exec_())
