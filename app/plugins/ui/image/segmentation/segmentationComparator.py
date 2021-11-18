from app.core.utils import SingletonDecorator
from app.core.ui import mainWindow as MW
from app.plugins.ui import sceneManagerUi as scm
from app.plugins.model.image.image import Image
from PyQt5 import Qt
import numpy as np
import matplotlib.pyplot as plt
from app.plugins.utils.image.colorMapUtils import colorDict, createColorMap
from app.plugins.utils.image.cmpPlot import CmpPlot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from PyQt5 import Qt, QtWidgets, QtCore, QtGui
from app.plugins.ui.image.segmentation.customDialog import CustomDialog
from app.plugins.ui.image.segmentation.pairingSpinesSegmentations import spinesSegmentationPairing as pairingSS
from scipy.ndimage.measurements import label as labelScipy

raw = None
label = None
pred = None

class SegmentationComparatorView(Qt.QWidget):
    def __init__(self, parent=None, rawImg=None, labelImg=None, predImg=None):
        Qt.QMainWindow.__init__(self, parent)
        self.raw = rawImg.img
        self.label = labelImg.img
        self.pred = predImg.img
        self.label = self.changeRangeImages(self.label)
        self.pred = self.changeRangeImages(self.pred)
        self.vl = Qt.QVBoxLayout(self)
        self.plotData()
        self.addOptions()

    def getElementsN(self, img, value, treshold=5, returnImg=False):
        structure = np.ones((3, 3, 3), dtype=np.int)
        arr = (img == value)
        labeled, prevcomponents = labelScipy(arr, structure)
        _, counts = np.unique(labeled, return_counts=True)
        elementsToRemove = np.where(counts < treshold)[0]
        for i in elementsToRemove:
            labeled[np.where(labeled == i)] = 0
        _, ncomponents = labelScipy(labeled != 0, structure)
        if returnImg:
            return labeled, ncomponents
        else:
            return ncomponents

    def changeRangeImages(self, img):
        changeOrder = False
        values = np.unique(img)
        values = values[values != 0]
        ncomponents0 = self.getElementsN(img, values[0])
        ncomponents1 = self.getElementsN(img, values[1])
        if ncomponents0 > ncomponents1:  # la etiqueta con menos elementos va a asumir que son dendritas y con más, espinas
            changeOrder = True
        if changeOrder:
            values = np.sort(values)[::-1]
        count = 1
        newArray = np.zeros((img.shape))
        for val in values:
            arr = np.multiply((img == val), count)
            newArray = np.add(newArray, arr)
            count+=1
        return newArray

    def plotData(self):
        # =============================================================================
        # Plot de resultados
        # =============================================================================
        cmcmp3 = createColorMap('cmcmp3', colorDict['cmp3'])
        cm3 = createColorMap('cm3', [(0.99, 0.99, 0.99), (0, 0.8, 0), (0, 0.5, 1)])
        cmc = createColorMap('cmc', [(0.95, 1, 0.95, 1), (0, 1, 0, 1)], N=255)
        cmap = (cm3, cmc, cm3, cmcmp3)

        cp = []

        cmpdata = (self.label, self.raw, self.pred, self.pred + self.label * 3)

        title = ["GT", "RAW", "PRED", "CMP"]

        cp.append(CmpPlot(cmpdata, 2, title=title, cmap=cmap, widget = self))

    def addOptions(self):
        pairingSegmentationButton = Qt.QPushButton('Pair segmentations')
        pairingSegmentationButton.clicked.connect(self.pairSegmentations)
        self.vl.addWidget(pairingSegmentationButton)

    def pairSegmentations(self):
        print('Pairing segmentations ')
        self._pair = pairingSS(self.pred, self.label)

    def addmpl(self, fig):
        canvas = FigureCanvas(fig)
        canvas.draw()

    def pltMP(self, img3d):
        img = np.max(img3d, axis=0)
        fig1 = Figure()
        ax = fig1.add_subplot(111)
        ax.imshow(img)

        self.addmpl(fig1)
        self.show()

@SingletonDecorator
class SegmentationComparator:
    def __init__(self, menuPath=None):
        self._mw = MW.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Segmentation"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$%$2"
        self._name = "Compare segmentation with GT"

        self._mw.addAction(self._name, prefix=self._prefix)
        self._mw.addActionCB(self._name,
                             self.selectImages,
                             prefix=self._prefix)
        self._mw.addAction2Menu(self._name,
                                menuPath=self._menuPath,
                                prefix=self._prefix)

    def selectImages(self):
        nodes = [n for n in self._smUI.selectedNodes if isinstance(n, Image) and n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")
        if len(nodes) != 3:
            self._mw.warningMsg('Please select raw, prediction and GT image')

        dlg = CustomDialog(nodes, ('Raw', 'Label', 'Prediction'))
        if dlg.exec_():
            print("Success!")
            segmentationComparatorView = SegmentationComparatorView(rawImg = dlg.imagesNode['Raw'],
            labelImg = dlg.imagesNode['Label'], predImg = dlg.imagesNode['Prediction'])
            self._mw.createDockableWidget(segmentationComparatorView, "Segmentation connector",
            dockAreaId = MW.DockAreaId.Right, hideOnClose = False)
        else:
            print("Cancel!")


def init(menuPath=None):
    SegmentationComparator(menuPath=menuPath)