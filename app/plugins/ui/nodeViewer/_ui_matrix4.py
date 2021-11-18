# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'matrix4.v2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_matrix4Viewer_form(object):
    def setupUi(self, matrix4Viewer_form):
        matrix4Viewer_form.setObjectName("matrix4Viewer_form")
        matrix4Viewer_form.resize(242, 92)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(matrix4Viewer_form.sizePolicy().hasHeightForWidth())
        matrix4Viewer_form.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(matrix4Viewer_form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.matrix_table = QtWidgets.QTableWidget(matrix4Viewer_form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matrix_table.sizePolicy().hasHeightForWidth())
        self.matrix_table.setSizePolicy(sizePolicy)
        self.matrix_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.matrix_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.matrix_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.matrix_table.setAutoScroll(True)
        self.matrix_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.matrix_table.setShowGrid(True)
        self.matrix_table.setGridStyle(QtCore.Qt.SolidLine)
        self.matrix_table.setWordWrap(False)
        self.matrix_table.setCornerButtonEnabled(False)
        self.matrix_table.setRowCount(3)
        self.matrix_table.setColumnCount(4)
        self.matrix_table.setObjectName("matrix_table")
        self.matrix_table.horizontalHeader().setVisible(False)
        self.matrix_table.horizontalHeader().setDefaultSectionSize(60)
        self.matrix_table.horizontalHeader().setHighlightSections(False)
        self.matrix_table.horizontalHeader().setMinimumSectionSize(60)
        self.matrix_table.verticalHeader().setVisible(False)
        self.matrix_table.verticalHeader().setDefaultSectionSize(30)
        self.matrix_table.verticalHeader().setHighlightSections(False)
        self.matrix_table.verticalHeader().setMinimumSectionSize(30)
        self.horizontalLayout.addWidget(self.matrix_table)

        self.retranslateUi(matrix4Viewer_form)

    # todo
    #        QtCore.QMetaObject.connectSlotsByName(matrix4Viewer_form)

    def retranslateUi(self, matrix4Viewer_form):
        _translate = QtCore.QCoreApplication.translate
        matrix4Viewer_form.setWindowTitle(_translate("matrix4Viewer_form", "Form"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    matrix4Viewer_form = QtWidgets.QWidget()
    ui = Ui_matrix4Viewer_form()
    ui.setupUi(matrix4Viewer_form)
    matrix4Viewer_form.show()
    sys.exit(app.exec_())
