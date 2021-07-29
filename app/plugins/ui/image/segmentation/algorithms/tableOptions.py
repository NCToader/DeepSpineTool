from PyQt5 import Qt
from app.core.ui import mainWindow as MW
import numpy as np

class TableOptions(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("contrastBrightnessEditor_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)
            self.to_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=parent)
            vLayout = Qt.QVBoxLayout()
            self.connectedCB = Qt.QCheckBox('Check sp-dendr connections')
            self.recalculateButton = Qt.QPushButton('Update table')
            self.diagonalsButton = Qt.QCheckBox('Diagonals count as same element')
            self.diagonalsButton.setChecked(False)
            vLayout.addWidget(self.connectedCB)
            vLayout.addWidget(self.diagonalsButton)
            self.to_layout.addLayout(vLayout)
            self.to_layout.addWidget(self.recalculateButton)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = TableOptions._UI(parent=self)
        self._viewer = viewer
        self._ui.recalculateButton.clicked.connect(self.recalculateTable)
        self._ui.connectedCB.stateChanged.connect(self.cbRecalculateState)
        self._ui.diagonalsButton.stateChanged.connect(self.cbDiagonalsState)


    def recalculateTable(self):
        self._viewer.updateLabels()

    def cbDiagonalsState(self, state):
        if state > 0:
            self._viewer.diagonalsConnected = True
        else:
            self._viewer.diagonalsConnected = False

    def cbRecalculateState(self, state):
        if state > 0:
            self._viewer.checkConnectedToDendrite = True
        else:
            self._viewer.checkConnectedToDendrite = False
