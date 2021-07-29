# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 11:21:25 2019

@author: URJC

#https://stackoverflow.com/questions/53135674/how-to-create-a-vertical-rotated-button-in-qt-with-c
"""
from PyQt5 import Qt
from enum import Enum, auto


class CollapsableWidget(Qt.QWidget):
    class Position(Enum):
        Top = auto()
        Bottom = auto()
        Left = auto()
        Right = auto()

    class _UI:
        def __init__(self, parent):
            # Main Widgets
            #############################################
            parent.setObjectName("colapsableWidget_form")
            parent.setSizePolicy(Qt.QSizePolicy.Expanding,
                                 Qt.QSizePolicy.Fixed)

            self.item_widget = Qt.QWidget(parent)
            self.item_widget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                           Qt.QSizePolicy.Fixed)
            self.item_widget.setObjectName("item_widget")

            # Creación de los layouts
            #############################################
            self.layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                        parent=parent)
            self.item_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                             parent=self.item_widget)

            self.layout.setSpacing(0)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.item_layout.setSpacing(0)
            self.item_layout.setContentsMargins(0, 0, 0, 0)

            self.layout.setSizeConstraint(Qt.QLayout.SetDefaultConstraint)
            self.layout.setObjectName("main_layout")
            self.item_layout.setSizeConstraint(Qt.QLayout.SetDefaultConstraint)
            self.item_layout.setObjectName("item_layout")

            # Elementos del interfaz
            #############################################
            self.collapse_toolButton = Qt.QToolButton(parent)
            self.collapse_toolButton.setSizePolicy(Qt.QSizePolicy.Expanding,
                                                   Qt.QSizePolicy.Fixed)

            ic = self.collapse_toolButton.iconSize() * 0.3
            self.collapse_toolButton.setIconSize(ic)

            self.collapse_toolButton.setAutoRaise(True)
            self.collapse_toolButton.setObjectName("collapse_toolButton")

            palette = self.collapse_toolButton.palette()
            #            palette.setBrush(Qt.QPalette.Base, Qt.Qt.darkGray)
            palette.setBrush(Qt.QPalette.Button, Qt.QColor(240, 240, 240))
            self.collapse_toolButton.setAutoFillBackground(True)
            self.collapse_toolButton.setPalette(palette)
            self.collapse_toolButton.update()

            # Configuración del layout
            #############################################
            self.layout.addWidget(self.collapse_toolButton)
            self.layout.addWidget(self.item_widget)

    def __init__(self, parent=None, position=Position.Bottom):
        if not isinstance(position, CollapsableWidget.Position):
            raise TypeError("ColapsableWidget.Area expected")

        # widget Init
        super().__init__(parent)
        self._ui = CollapsableWidget._UI(self)

        self._showing = True

        self._position = position
        self._setPosition()

        self._ui.collapse_toolButton.clicked.connect(self._collapseButtonPress)

    def _setArrow(self):
        arrow = self._showedArrow if self._showing else self._hiddenArrow
        self._ui.collapse_toolButton.setArrowType(arrow)

    def _setPosition(self):
        if self._position == CollapsableWidget.Position.Top:
            self._showedArrow = Qt.Qt.UpArrow
            self._hiddenArrow = Qt.Qt.DownArrow
            xPol = Qt.QSizePolicy.Expanding
            yPol = Qt.QSizePolicy.Fixed

            dir_ = Qt.QBoxLayout.BottomToTop


        elif self._position == CollapsableWidget.Position.Bottom:
            self._hiddenArrow = Qt.Qt.UpArrow
            self._showedArrow = Qt.Qt.DownArrow
            xPol = Qt.QSizePolicy.Expanding
            yPol = Qt.QSizePolicy.Fixed

            dir_ = Qt.QBoxLayout.TopToBottom

        elif self._position == CollapsableWidget.Position.Left:
            self._hiddenArrow = Qt.Qt.RightArrow
            self._showedArrow = Qt.Qt.LeftArrow

            yPol = Qt.QSizePolicy.Expanding
            xPol = Qt.QSizePolicy.Fixed

            dir_ = Qt.QBoxLayout.RightToLeft

        elif self._position == CollapsableWidget.Position.Right:
            self._hiddenArrow = Qt.Qt.LeftArrow
            self._showedArrow = Qt.Qt.RightArrow

            yPol = Qt.QSizePolicy.Expanding
            xPol = Qt.QSizePolicy.Fixed

            dir_ = Qt.QBoxLayout.LeftToRight

        self.setSizePolicy(xPol, yPol)
        self._ui.item_widget.setSizePolicy(xPol, yPol)
        self._ui.collapse_toolButton.setSizePolicy(xPol, yPol)
        self._ui.layout.setDirection(dir_)
        self._ui.item_layout.setDirection(dir_)
        self._setArrow()

    @Qt.pyqtSlot()
    def _collapseButtonPress(self):
        self.showWidgets = not self.showWidgets

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not isinstance(value, CollapsableWidget.Position):
            raise TypeError("ColapsableWidget.Position expected")
        self._position = value
        self._setPosition()

    @property
    def showCollapseButton(self):
        return self._ui.collapse_toolButton.isVisible()

    @showCollapseButton.setter
    def showCollapseButton(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._ui.collapse_toolButton.setVisible(value)

    @property
    def showWidgets(self):
        return self._showing

    @showWidgets.setter
    def showWidgets(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")

        self._showing = value
        self._setArrow()
        self._ui.item_widget.setVisible(self._showing)

    def addWidget(self, widget):
        if not isinstance(widget, Qt.QWidget):
            raise TypeError("QWidget expected")

        widget.setParent(self._ui.item_widget)
        self._ui.item_layout.addWidget(widget)

    def getWidgets(self):
        return [self._ui.item_layout.itemAt(i).widget() \
                for i in range(self._ui.item_layout.count()) \
                if self._ui.item_layout.itemAt(i).widget() is not None]


if __name__ == '__main__':
    import sys

    #    import numpy as np

    app = Qt.QApplication(sys.argv)
    ex = CollapsableWidget()
    ex.show()
    ex.addWidget(Qt.QPushButton("B1"))
    ex.position = CollapsableWidget.Position.Right
    #    ex.showCollapseButton = False

    print(ex.getWidgets())

    sys.exit(app.exec())
