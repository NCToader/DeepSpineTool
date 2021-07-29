import time

from PyQt5 import Qt, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from scipy.ndimage.measurements import label
from app.core.ui import mainWindow as MW
from app.core.utils import SingletonDecorator

from app.plugins.ui.image.viewer.img3Viewer import Img3Viewer
from app.plugins.model.image.image import Image
from app.core.model import scene as SC
from app.plugins.ui import sceneManagerUi as scm
from app.plugins.utils.image.colorMapUtils import createColorMap
import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.ndimage.measurements import label as labelScipy
DEBUG_INFO = True


class NoiseFilterManager(Qt.QWidget):
    def __init__(self, segViewer, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._mw = MW.MainWindow()
        self.viewer = segViewer
        self.editedImg = self.viewer._imageNode
        #self.editedImg.img = np.copy(segViewer.img)
        self.spacing = (0.279911, 0.0751562, 0.0751562)
        self.initImg = np.zeros(self.editedImg.img.shape, dtype=np.uint16)
        self.changeRangeImages(self.editedImg.img)
        self.showArray = np.copy(self.initImg)
        #self.editedImg.img= np.copy(self.initImg)
        map = createColorMap('label', [(0.99, 0.99, 0.99), (0, 1.0, 0.5), (0, 0.5, 1)])
        segViewer.renderer.setPlotParams(cmap=map)
        #editedViewer.renderer.setPlotParams(cmap=map)

        self.pltOptions()
        self.viewer.renderer._fig.canvas.mpl_connect('key_press_event', self.onpress)


    def pltOptions(self):
        vLayout1 = QtWidgets.QVBoxLayout()
        vLayout = QtWidgets.QVBoxLayout()
        hLayout1 = QtWidgets.QHBoxLayout()
        hLayout2 = QtWidgets.QVBoxLayout()
        hLayout3 = QtWidgets.QVBoxLayout()

        self.editSpines = Qt.QCheckBox('Apply to spines')
        self.editSpines.setChecked(True)
        self.editDendrites = Qt.QCheckBox('Apply to dendrites')
        self.editDendrites.setChecked(True)
        vLayout1.addWidget(self.editSpines)
        vLayout1.addWidget(self.editDendrites)

        minVolLabel = Qt.QLabel('Min. volume')
        self.minVol = Qt.QLineEdit('0')
        hLayout1.addWidget(minVolLabel)
        hLayout1.addWidget(self.minVol)

        minDistLabel = Qt.QLabel('Min. distance')
        self.minDist = Qt.QLineEdit('0')
        minDistLabel2 = Qt.QLabel(' to dendrite with volume')
        self.bigDendrVol = Qt.QLineEdit('0')
        hLayout2.addWidget(minDistLabel)
        hLayout2.addWidget(self.minDist)
        hLayout2.addWidget(minDistLabel2)
        hLayout2.addWidget(self.bigDendrVol)

        applyButton = Qt.QPushButton('Apply')
        resetButton = Qt.QPushButton('Reset')
        hLayout3.addWidget (applyButton)
        hLayout3.addWidget(resetButton)

        vLayout.addLayout(vLayout1)
        vLayout.addLayout(hLayout1)
        vLayout.addLayout(hLayout2)
        vLayout.addLayout(hLayout3)
        self.setLayout(vLayout)

        applyButton.clicked.connect(self.applyEditions)
        resetButton.clicked.connect(self.resetEditions)

    def applyEditions(self):
        self.removeCategorySmallerTreshold()
        self.removeSpDistTreshold()
        self.editedImg.img = self.showArray

    def resetEditions(self):
        self.editedImg.img = self.initImg
        self.showArray = self.editedImg.img

    def getElementsN(self, arr, treshold=5, returnImg=False):
        structure = np.ones((3, 3, 3), dtype=np.int)
        labeled, prevcomponents = labelScipy(arr, structure)
        _, counts = np.unique(labeled, return_counts=True)
        elementsToRemove = np.where(counts < treshold)[0]
        for i in elementsToRemove:
            labeled[np.where(labeled == i)] = 0
        _, ncomponents = labelScipy(labeled != 0, structure)
        if DEBUG_INFO:
            print('Previous elements ', prevcomponents)
            print('Elements after removing ', ncomponents)
            print('Total elements removed ', prevcomponents - ncomponents)
        if returnImg:
            return labeled, ncomponents
        else:
            return ncomponents

    def changeRangeImages(self, img):
        changeOrder = False
        values = np.unique(img)
        values = values[values != 0]

        ncomponents0 = self.getElementsN(img==values[0] , treshold=0)
        ncomponents1 = self.getElementsN(img==values[1] , treshold=0)

        if ncomponents0 > ncomponents1:  # la etiqueta con menos elementos va a asumir que son dendritas y con más, espinas
            changeOrder = True
        if changeOrder:
            values = np.sort(values)[::-1]
        count = 1
        newArray = np.zeros((img.shape))
        for val in values:
            arr = np.multiply((img == val), count)
            newArray = np.add(newArray, arr)
            count += 1
        self.initImg = np.copy(newArray).astype(np.uint16)

    def removeCategorySmallerTreshold(self):
        if int(self.minVol.text())==0:
            return
        imgDendr = (self.showArray == 1)
        imgSpine = (self.showArray == 2)
        if self.editDendrites.isChecked():
            imgDendr, _ = self.getElementsN(imgDendr, treshold=int(self.minVol.text()), returnImg=True)
            print('Pixeles dendrita ', np.count_nonzero(imgDendr), '\n')
        if self.editSpines.isChecked():
            imgSpine, _ = self.getElementsN(imgSpine, treshold=int(self.minVol.text()), returnImg=True)
            print('Pixeles espina ', np.count_nonzero(imgSpine), '\n')
        mask = np.add(imgDendr, imgSpine).astype(bool)
        self.showArray= np.multiply(self.showArray, mask)

    def removeSpDistTreshold(self):
        if int(self.minDist.text())==0:
            return
        imgDendr = (self.showArray==1)
        if int(self.bigDendrVol.text())>0:
            imgDendr = self.getElementsN(imgDendr, treshold=int(self.bigDendrVol.text()), returnImg=True)[0]
        imgDendr = np.invert(imgDendr.astype(bool))
        d = distance_transform_edt(imgDendr, sampling=self.spacing)
        dMask = [d < float(self.minDist.text())][0]
        self.showArray = self.showArray * dMask

    def onpress(self, event):
        if event.key == 'ctrl+r':
            print('Vis changed')
            self.viewer.img = self.initImg
        elif event.key == 'ctrl+a':
            print('Vis changed')
            self.viewer.img = self.showArray

class ViewSplitter(Qt.QSplitter):
    def __init__(self, parent=None, segImg=None, manager = None):
        Qt.QMainWindow.__init__(self, parent)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(segImg)
        self.addWidget(manager)


@SingletonDecorator
class NoiseEditor:
    def __init__(self, menuPath=None):
        self._mw = MW.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Segmentation"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$%$2"
        self._name = "Noise filter"

        self._mw.addAction(self._name, prefix=self._prefix)
        self._mw.addActionCB(self._name,
                             self.selectPredictionImage,
                             prefix=self._prefix)
        self._mw.addAction2Menu(self._name,
                                menuPath=self._menuPath,
                                prefix=self._prefix)

    def addViewer(self, segView):

        nMan = NoiseFilterManager(segView)

        viewSplitter = ViewSplitter(segImg=segView, manager=nMan)

        self._mw.createDockableWidget(viewSplitter,
                                      "Noise filter",
                                      dockAreaId=MW.DockAreaId.Right,
                                      hideOnClose=False)

    def selectPredictionImage(self):
        nodes = [n for n in self._smUI.selectedNodes if isinstance(n, Image) and n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")
        if len(nodes) == 1:
            segView = Img3Viewer(nodes[0])
            # editedImgNode = Image(name='edition_' + nodes[0].name)
            # SC.Scene().addNode2Parent(editedImgNode, parent=nodes[0])
            # editedView = Img3Viewer(editedImgNode)
            self.addViewer(segView)
        elif len(nodes)>=2:
            self._mw.warningMsg('Please select only one image')


def init(menuPath=None):
    NoiseEditor(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys

    app = Qt.QApplication(sys.argv)

    #todo
    sys.exit(app.exec())
