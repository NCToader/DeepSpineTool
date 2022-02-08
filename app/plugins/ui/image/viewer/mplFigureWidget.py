# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 18:59:52 2019

@author: Marcos García
#!todo: Añadir un toolbar para la edición de la figura, scrollbars... ocultar cosas...
#!todo: Labels verticales. Ver enlace
https://stackoverflow.com/questions/9183050/vertical-qlabel-or-the-equivalent
#!todo: hay funciones que se pueden transformar en propiedades
https://matplotlib.org/2.0.0/api/backend_qt5agg_api.html#matplotlib.backends.backend_qt5agg.FigureCanvasQTAggBase
https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_qt_sgskip.html
https://matplotlib.org/gallery/user_interfaces/embedding_in_qt5_sgskip.html
https://pythonspot.com/pyqt5-matplotlib/

https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html
"""

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

from PyQt5 import Qt, QtCore
from enum import Enum

# import matplotlib
##matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar2
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from app.plugins.ui.qbasics import CollapsableWidget


class MplFigureWidget(Qt.QWidget):
    class WidgetArea(Enum):
        TopLeft = (0, 0)
        Top = (0, 1)
        TopRight = (0, 2)
        Left = (1, 0)
        Right = (1, 2)
        BottomLeft = (2, 0)
        Bottom = (2, 1)
        BottomRight = (2, 2)

    class ToolbarPosition(Enum):
        Top = CollapsableWidget.Position.Top
        Bottom = CollapsableWidget.Position.Bottom
        Left = CollapsableWidget.Position.Left
        Right = CollapsableWidget.Position.Right

    minimunSize = (100, 100)

    class UI:
        def __init__(self, parent, figure):
            parent.setObjectName("mplFigure_form")

            # Creación de los layouts
            self.layout = Qt.QGridLayout(parent)
            self.layout.setSizeConstraint(Qt.QLayout.SetDefaultConstraint)
            self.layout.setObjectName("main_layout")

            self.central_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom)
            self.central_layout.setSizeConstraint(Qt.QLayout.SetDefaultConstraint)
            self.central_layout.setObjectName("central_layout")

            self.title_layout = Qt.QBoxLayout(Qt.QBoxLayout.BottomToTop)
            self.title_layout.setSizeConstraint(Qt.QLayout.SetDefaultConstraint)
            self.title_layout.setObjectName("title_layout")

            # Elementos de widget
            self.figure_scrollArea = Qt.QScrollArea(parent)
            self.figure_scrollArea.setWidgetResizable(True)
            self.figure_canvas = FigureCanvas(figure)
            self.figure_canvas.setObjectName("figure_canvas")
            self.figure_canvas.setParent(self.figure_scrollArea)
            self.figure_canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.figure_canvas.setFocus()
            self.figure_canvas.setSizePolicy(Qt.QSizePolicy.Expanding,
                                             Qt.QSizePolicy.Expanding)
            self.figure_canvas.setMinimumSize(*MplFigureWidget.minimunSize)
            self.figure_scrollArea.setWidget(self.figure_canvas)

            self.toolbar_form = CollapsableWidget(parent,
                                                  position=CollapsableWidget.Position.Bottom)

            self.toolbar = NavigationToolbar2(self.figure_canvas,
                                             self.toolbar_form,
                                             coordinates=True)
            self.toolbar_form.addWidget(self.toolbar)

            self.title_form = CollapsableWidget(parent,
                                                position=CollapsableWidget.Position.Top)
            self.title_label = Qt.QLabel(self.title_form)
            self.title_label.setText("Title")
            self.title_label.setAlignment(Qt.Qt.AlignCenter)
            self.title_form.addWidget(self.title_label)

            # Configuración de los layouts
            self.central_layout.addWidget(self.figure_scrollArea)
            self.central_layout.addWidget(self.toolbar_form)

            self.title_layout.addLayout(self.central_layout)
            self.title_layout.addWidget(self.title_form)

            self.layout.addWidget(Qt.QWidget(parent), 0, 0)
            self.layout.addWidget(Qt.QWidget(parent), 0, 1)
            self.layout.addWidget(Qt.QWidget(parent), 0, 2)
            self.layout.addWidget(Qt.QWidget(parent), 1, 0)
            self.layout.addLayout(self.title_layout, 1, 1)
            self.layout.addWidget(Qt.QWidget(parent), 1, 2)
            self.layout.addWidget(Qt.QWidget(parent), 2, 0)
            self.layout.addWidget(Qt.QWidget(parent), 2, 1)
            self.layout.addWidget(Qt.QWidget(parent), 2, 2)
            self.layout.setVerticalSpacing(0)
            self.layout.setHorizontalSpacing(0)
            self.layout.setContentsMargins(0, 0, 0, 0)

        def getToolbar(self):
            nvtb = NavigationToolbar2(self.figure_canvas,
                                             self.toolbar_form,
                                             coordinates=True)
            def newHome():
                print('New home')
            nvtb.actions()[0].triggered.connect(newHome)
            return nvtb

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent)
        self._figure = Figure(*args, **kwargs)
        self._ui = MplFigureWidget.UI(self, self._figure)

        self._showCoordinates = True
        self._toolbarPosition = MplFigureWidget.ToolbarPosition.Bottom
        self._setToolbarPosition()

        self._titlePosition = MplFigureWidget.ToolbarPosition.Top
        self._setTitlePosition()


    def _setTitlePosition(self):
        v = self._titlePosition
        self._ui.title_form.position = v.value

        if MplFigureWidget.ToolbarPosition.Top == v:
            self._ui.title_layout.setDirection(Qt.QBoxLayout.BottomToTop)
        elif MplFigureWidget.ToolbarPosition.Bottom == v:
            self._ui.title_layout.setDirection(Qt.QBoxLayout.TopToBottom)
        elif MplFigureWidget.ToolbarPosition.Left == v:
            self._ui.title_layout.setDirection(Qt.QBoxLayout.RightToLeft)
        elif MplFigureWidget.ToolbarPosition.Right == v:
            self._ui.title_layout.setDirection(Qt.QBoxLayout.LeftToRight)

    def _setToolbarPosition(self):
        v = self._toolbarPosition
        self._ui.toolbar_form.position = v.value

        if MplFigureWidget.ToolbarPosition.Top == v:
            self._ui.toolbar.setOrientation(Qt.Qt.Horizontal)
            self._ui.central_layout.setDirection(Qt.QBoxLayout.BottomToTop)
            self._ui.toolbar.coordinates = self._showCoordinates
        elif MplFigureWidget.ToolbarPosition.Bottom == v:
            self._ui.toolbar.setOrientation(Qt.Qt.Horizontal)
            self._ui.central_layout.setDirection(Qt.QBoxLayout.TopToBottom)
            self._ui.toolbar.coordinates = self._showCoordinates
        elif MplFigureWidget.ToolbarPosition.Left == v:
            self._ui.toolbar.setOrientation(Qt.Qt.Vertical)
            self._ui.central_layout.setDirection(Qt.QBoxLayout.RightToLeft)
            self._ui.toolbar.coordinates = False
        elif MplFigureWidget.ToolbarPosition.Right == v:
            self._ui.toolbar.setOrientation(Qt.Qt.Vertical)
            self._ui.central_layout.setDirection(Qt.QBoxLayout.LeftToRight)
            self._ui.toolbar.coordinates = False

    def getSideWidget(self, area):
        if not isinstance(area, MplFigureWidget.WidgetArea):
            raise TypeError("MplFigureWidget.WidgetArea expected")

        r, c = area.value
        return self._layout.itemAtPosition(r, c).widget()

    def setSideWidget(self, area, widget):
        if not isinstance(area, MplFigureWidget.WidgetArea):
            raise TypeError("MplFigureWidget.WidgetArea expected")

        if not isinstance(area, Qt.QWidget):
            raise TypeError("Qt.QWidget expected")

        r, c = area.value()
        self._ui.layout.itemAtPosition(r, c).widget().deleteLater()
        self._ui.layout.addWidget(widget, r, c)

    @property
    def spacing(self):
        r = self._ui.layout.getVerticalSpacing()
        c = self._ui.layout.getHorizontalSpacing()
        return (r, c)

    @spacing.setter
    def spacing(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Tuple expected")
        if len(value) != 2:
            raise AttributeError("Unexpected length (2)")

        row, col = value
        self._ui.layout.setVerticalSpacing(col)
        self._ui.layout.setHorizontalSpacing(row)

    @property
    def margins(self):
        m = self._ui.layout.contentsMargins()

        return (m.left, m.top, m.right, m.bottom)

    @margins.setter
    def margins(self, value):
        "left, top, right, bottom"
        if not isinstance(value, tuple):
            raise TypeError("Tuple expected")
        if len(value) != 4:
            raise AttributeError("Unexpected length (2)")

        left, top, right, bottom = value
        self._ui.layout.setContentsMargins(left, top, right, bottom)

    @property
    def figureCanvasMininumSize(self):
        size = self._ui.figure_canvas.minimumSize()
        return (size.width(), size.height())

    @figureCanvasMininumSize.setter
    def figureCanvasMininumSize(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Tuple expected")
        if len(value) != 2:
            raise AttributeError("Unexpected length (2)")

        xPix, yPix = value
        self._ui.figure_canvas.setMinimumSize(xPix, yPix)

    @property
    def showCoordinates(self):
        return self._ui.toolbar_form.coordinates

    @showCoordinates.setter
    def showCoordinates(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._showCoordinates = value
        if self._toolbarPosition in (MplFigureWidget.ToolbarPosition.Top,
                                     MplFigureWidget.ToolbarPosition.Bottom):
            self._ui.toolbar.coordinates = self._showCoordinates
        else:
            self._ui.toolbar.coordinates = False

    @property
    def showToolbar(self):
        return self._ui.toolbar_form.isVisible()

    @showToolbar.setter
    def showToolbar(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        if value:
            self._ui.toolbar_form.show()
        else:
            self._ui.toolbar_form.hide()

    @property
    def showToolbarCollapseButton(self):
        return self._ui.toolbar_form.showCollapseButton

    @showToolbarCollapseButton.setter
    def showToolbarCollapseButton(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._ui.toolbar_form.showCollapseButton = value

    @property
    def showTitle(self):
        return self._ui.title_form.isVisible()

    @showTitle.setter
    def showTitle(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        if value:
            self._ui.title_form.show()
        else:
            self._ui.title_form.hide()

    @property
    def showTitleCollapseButton(self):
        return self._ui.title_form.showCollapseButton

    @showTitleCollapseButton.setter
    def showTitleCollapseButton(self, value):
        if not isinstance(value, bool):
            raise TypeError("Boolean expected")
        self._ui.title_form.showCollapseButton = value

    @property
    def toolbarPosition(self):
        return self._toolbarPosition

    @toolbarPosition.setter
    def toolbarPosition(self, value):
        if not isinstance(value, MplFigureWidget.ToolbarPosition):
            raise TypeError("Boolean expected")
        self._toolbarPosition = value
        self._setToolbarPosition()

    @property
    def titlePosition(self):
        return self._titlePosition

    @titlePosition.setter
    def titlePosition(self, value):
        if not isinstance(value, MplFigureWidget.ToolbarPosition):
            raise TypeError("Boolean expected")
        self._titlePosition = value
        self._setTitlePosition()

    @property
    def figureVerticalScrollBarPolicy(self):
        return self._ui.figure_scrollArea.verticalScrollBarPolicy()

    @figureVerticalScrollBarPolicy.setter
    def figureVerticalScrollBarPolicy(self, value):
        self._ui.figure_scrollArea.setVerticalScrollBarPolicy(value)

    @property
    def figureHorizontalScrollBarPolicy(self):
        return self._ui.figure_scrollArea.horizontalScrollBarPolicy()

    @figureHorizontalScrollBarPolicy.setter
    def figureHorizontalScrollBarPolicy(self, value):
        self._ui.figure_scrollArea.setHorizontalScrollBarPolicy(value)

    @property
    def figureCanvasResizable(self):
        return self._ui.figure_scrollArea.widgetResizable()

    @figureCanvasResizable.setter
    def figureCanvasResizable(self, value):
        self._ui.figure_scrollArea.setWidgetResizable(value)

    @property
    def titleLabel(self):
        return self._ui.title_label

    @property
    def figure(self):
        return self._figure

    @property
    def toolbar(self):
        return self._ui.toolbar

if __name__ == '__main__':
    #    try:
    import sys
    import numpy as np

    app = Qt.QApplication(sys.argv)
    ex = MplFigureWidget(figsize=(5, 3))  # , dpi = 300)
    #        ex.showToolbar= False
    #        ex.showToolbar = True
    ex.toolbarPosition = MplFigureWidget.ToolbarPosition.Top
    ex.showCoordinates = True
    ex.titlePosition = MplFigureWidget.ToolbarPosition.Bottom
    ex.figureCanvasMininumSize = (300, 300)
    ex.figureHorizontalScrollBarPolicy = Qt.Qt.ScrollBarAlwaysOff
    ex.figureVerticalScrollBarPolicy = Qt.Qt.ScrollBarAlwaysOff
    #        ex.figureCanvasResizable = False
    #        ex.showToolbarCollapseButton = False
    #        ex.showTitleCollapseButton = False
    #        ex.showTitle = False

    t = np.linspace(0, 10, 501)
    ex.figure.subplots().plot(t, np.tan(t), ".")

    ex.show()
    sys.exit(app.exec())
