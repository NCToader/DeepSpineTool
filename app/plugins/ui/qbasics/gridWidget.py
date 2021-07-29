# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 18:19:27 2019

@author: Marcos García
#!todo: Clase por desarrollar, poner un toolbar, menu contextual...
#!todo: Cuando se elimina un widget, no se elimina de la lista de widgets.
        Conectar la señal de destrucción a la eliminación del widget
#!todo: Cambiar la función de resize para que comporte como un tabla 
#       (filas y columnas)
#!todo: Investigar para que el borde del handle tenga una anchura de 0.
        
"""

from PyQt5 import Qt

from enum import Enum, auto
import numbers as num
import math as mt
import copy as cp


class GridWidget(Qt.QWidget):
    class Orientation(Enum):
        SingleRow = auto()
        SingleCol = auto()
        Grid = auto()

    class Policy(Enum):
        #               Rows   Cols
        AdjustCols = (False, True)
        AdjustRows = (True, False)
        AdjustAll = (True, True)

    class _UI:
        def __init__(self, parent):
            # Main Widgets
            #############################################
            parent.setObjectName("gridWidget_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            #            parent.setStyleSheet(
            #                    "QSplitter::handle{background-color: rgb(0, 0, 0);}")

            self.row_splitter = Qt.QSplitter(Qt.Qt.Vertical, parent=parent)
            self.row_splitter.setObjectName("row_splitter")
            self.col_splitterArray = []

            # Creación de los layouts
            #############################################
            #            self.layout = Qt.QGridLayout(parent = parent)
            self.layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                        parent=parent)

            #            self.layout.setSpacing(0)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setObjectName("main_layout")

            self.layout.addWidget(self.row_splitter)

    def __init__(self, parent=None):
        # widget Init
        super().__init__(parent)
        self._ui = GridWidget._UI(self)

        self._widgets = []
        self._nrows = 0
        self._ncols = 0
        self._fix = False
        self._width = 4

        self._orientation = GridWidget.Orientation.Grid
        self._policy = GridWidget.Policy.AdjustAll

    @property
    def policy(self):
        return self._policy

    @policy.setter
    def policy(self, value):
        if not isinstance(value, GridWidget.Policy):
            raise TypeError("GridWidget.Policy expected")

        if self._policy != value:
            if self._orientation == GridWidget.Orientation.Grid:
                self._policy = value
                self._updateGrid()

            elif self._orientation == GridWidget.Orientation.SingleCol:
                if not value.value[1]:
                    self._policy = value
                    self._updateGrid()

            elif self._orientation == GridWidget.Orientation.SingleRow:
                if not value.value[0]:  # Filas fijas
                    self._policy = value
                    self._updateGrid()

    @property
    def nrows(self):
        return self._nrows

    @nrows.setter
    def nrows(self, value):
        self._checkPositiveInt(value)

        if self._orientation == GridWidget.Orientation.Grid and \
                self._nrows != value:
            self._nrows = value
            self._updateGrid()

    @property
    def ncols(self):
        return self._ncols

    @ncols.setter
    def ncols(self, value):
        self._checkPositiveInt(value)

        if self._orientation == GridWidget.Orientation.Grid and \
                self._ncols != value:
            self._ncols = value
            self._updateGrid()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if not isinstance(value, GridWidget.Orientation):
            raise TypeError("GridWidget.Orientation expected")

        if self._orientation != value:

            if value == GridWidget.Orientation.SingleRow:
                self._policy = GridWidget.Policy.AdjustCols

            elif value == GridWidget.Orientation.SingleCol:
                self._policy = GridWidget.Policy.AdjustRows

            self._orientation = value
            self._updateGrid()

    @property
    def widgets(self):
        return tuple(self._widgets)

    @property
    def fix(self):
        return self._fix

    @fix.setter
    def fix(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        if self._fix != value:
            self._fix = value
            self._updateGrid()

    @property
    def splitterWidth(self):
        return self._width

    @splitterWidth.setter
    def splitterWidth(self, value):
        if not isinstance(value, num.Integral):
            raise TypeError("Integer expected")

        if value < 0:
            raise AttributeError("Positive value expected")

        if self._width != value:
            self._width = value
            self._updateGrid()

    @property
    def contentsMargin(self):
        cm = self._ui.layout.contentsMargins()
        return cm.left(), cm.top(), cm.right(), cm.bottom()

    @contentsMargin.setter
    def contentsMargin(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Tuple expected")

        if len(value) != 4:
            raise AttributeError("4 element tuple expected")

        self._ui.layout.setContentsMargins(*value)

    def widgetInserted(self, widget):
        self._checkWidget(widget)
        return (widget in self._widgets)

    def addWidget(self, widget):
        self._checkWidget(widget)

        if widget not in self._widgets:
            self._widgets.append(widget)
            self._updateGrid()

    def insertWidget(self, pos, widget):
        self._checkWidget(widget)

        if widget not in self._widgets:
            self._widgets.insert(pos, widget)
            self._updateGrid()

    def clearAllWidgets(self, delete=True):
        self._deattachWidgets()

        for w in self._widgets:
            w.setParent(None)
            if (delete): w.deleteLater()

        self._widgets = []
        self._updateGrid()

    def removeWidget(self, widget, delete=True):
        self._checkWidget(widget)

        if widget in self._widgets:
            widget.setParent(None)

            if (delete): widget.deleteLater()

            self._widgets.remove(widget)
            self._updateGrid()

    def sortWidgets(self, **kwargs):
        self._widgets.sort(**kwargs)
        self._updateGrid()

    @staticmethod
    def _checkWidget(widget):
        if not isinstance(widget, Qt.QWidget):
            raise TypeError("QWidget expected")

    @staticmethod
    def _checkPositiveInt(i):
        if not isinstance(i, num.Integral):
            raise TypeError("Integer expected")
        elif i < 0:
            raise ValueError("Positive value expected")

    @staticmethod
    def _enableSplitter(splitter, on=True):
        for i in range(splitter.count()):
            splitter.handle(i).setEnabled(on)

    @staticmethod
    def _setHandleColor(splitter):
        for i in range(splitter.count()):
            pal = splitter.handle(i).palette()
            pal.setBrush(Qt.QPalette.Window, Qt.QColor(230, 230, 230))
            splitter.handle(i).setAutoFillBackground(True)
            splitter.handle(i).setPalette(pal)
            splitter.handle(i).update()

    #    @staticmethod
    #    def _hideSplitter(splitter):
    #        for i in range(splitter.count()):
    #            splitter.handle(i).hide()

    def _deattachWidgets(self):
        for w in self._widgets:
            w.setParent(None)

    def _clearWindow(self):
        self._deattachWidgets()

        for c in self._ui.col_splitterArray:
            c.deleteLater()

        self._ui.col_splitterArray = []

    def _updateGrid(self):
        self._clearWindow()

        if len(self.widgets) == 0:
            self._ncols = 0
            self._nrows = 0
            return

        # Ajustes de las columnas  
        ######################################        
        slots = self._nrows * self._ncols
        nwidgets = len(self._widgets)

        if self._orientation == GridWidget.Orientation.SingleCol:
            self._ncols = 1
        elif self._orientation == GridWidget.Orientation.SingleRow:
            self._nrows = 1

        if slots > nwidgets or slots < nwidgets:
            if self._policy.value[0] and self._policy.value[1]:
                self._ncols = int(mt.ceil(mt.sqrt(nwidgets)))
                self._nrows = int(mt.ceil(nwidgets / self._ncols))
            elif self._policy.value[0]:
                self._nrows = int(mt.ceil(nwidgets / self._ncols))
            elif self._policy.value[1]:
                self._ncols = int(mt.ceil(nwidgets / self._nrows))

        # Pintado
        ######################################        
        slots = self._nrows * self._ncols
        widgets = cp.copy(self._widgets)
        widgets.extend([Qt.QWidget() for i in range(slots - nwidgets)])

        if self._policy == GridWidget.Policy.AdjustCols:
            for i in range(self._nrows):
                col_splitter = \
                    Qt.QSplitter(Qt.Qt.Horizontal)
                self._ui.col_splitterArray.append(col_splitter)
                self._ui.row_splitter.addWidget(col_splitter)

            k = 0
            for j in range(self._ncols):
                for i in range(self._nrows):
                    col_splitter = self._ui.col_splitterArray[i]
                    col_splitter.addWidget(widgets[k])
                    k = k + 1
        else:
            k = 0
            for i in range(self._nrows):
                col_splitter = \
                    Qt.QSplitter(Qt.Qt.Horizontal)
                self._ui.col_splitterArray.append(col_splitter)
                self._ui.row_splitter.addWidget(col_splitter)

                for j in range(self._ncols):
                    col_splitter.addWidget(widgets[k])
                    k = k + 1

                    # Fix and handle width
        ######################################  
        self._enableSplitter(self._ui.row_splitter, on=not self._fix)
        self._setHandleColor(self._ui.row_splitter)
        self._ui.row_splitter.setHandleWidth(self._width)
        #        if self._width == 0 or self._width == 1:
        #            self._ui.row_splitter.setLineWidth(0)
        #            self._ui.row_splitter.setMidLineWidth(0)
        #            self._hideSplitter(self._ui.row_splitter)

        for c in self._ui.col_splitterArray:
            self._enableSplitter(c, on=not self._fix)
            self._setHandleColor(c)
            c.setHandleWidth(self._width)


#            if self._width == 0 or self._width == 1:
#                self._hideSplitter(c)


if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)
    ex = GridWidget()
    ex.show()
    ex.addWidget(Qt.QPushButton("B1"))
    ex.addWidget(Qt.QPushButton("B2"))
    ex.addWidget(Qt.QPushButton("B3"))
    ex.addWidget(Qt.QPushButton("B4"))
    ex.addWidget(Qt.QPushButton("B5"))
    b = Qt.QPushButton("B6")
    ex.addWidget(b)
    ex.removeWidget(b)

    #    ex.orientation = GridWidget.Orientation.SingleRow
    ex.policy = GridWidget.Policy.AdjustCols
    ex.nrows = 4
    #    ex.fix = True
    ex.splitterWidth = 4

    print(ex.ncols, ex.nrows)
    print(ex.policy)
    print(ex.orientation)
    print(ex.widgets)
    print(ex.contentsMargin)
    print(ex.fix)

    sys.exit(app.exec())
