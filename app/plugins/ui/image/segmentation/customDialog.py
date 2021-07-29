from PyQt5 import Qt
from app.core.ui import mainWindow as MW
import numpy as np

class CustomDialog(Qt.QDialog):

    def __init__(self, nodes, imageTypes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = MW.MainWindow()
        self.setWindowTitle("Choose corresponding images")
        self.nodes = np.copy(nodes)
        self.imagesNode = dict()

        form = Qt.QFormLayout(self)
        buttons = []
        lineEdits = []

        for i in range(len(nodes)):
            bt = Qt.QPushButton('Choose ' + imageTypes[i] + ' image')
            le = Qt.QLineEdit()
            buttons.append(bt)
            lineEdits.append(le)
            form.addRow(bt, le)

        for i in range(len(buttons)):
            buttons[i].clicked.connect(lambda _, i=i: self.getItem(imageTypes[i], lineEdits[i]))

        buttonBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok | Qt.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        form.addRow(buttonBox)


    def getItem(self, imageType, le):
        items = [n.name for n in self.nodes]
        dialogTitle = 'Select ' + imageType + ' image'
        item, ok = Qt.QInputDialog.getItem(self._mw, 'Select image', dialogTitle, items, 0, False)
        if ok and item:
            le.setText(item)
            self.imagesNode[imageType] = self.nodes[items.index(item)]
        else:
            self._mw.warningMsg('Nothing selected')