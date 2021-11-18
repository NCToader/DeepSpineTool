from PyQt5 import Qt, QtWidgets, QtCore
import numpy as np
from app.plugins.utils.image.image import getAABBImg, idxAABB, ellipStruct
from app.core.ui import mainWindow as MW
from app.plugins.utils.image.AStar import labeledImgAStar
from skimage.segmentation import find_boundaries, flood
from scipy.ndimage.filters import median_filter
from app.plugins.ui import sceneManagerUi as scm
from scipy.ndimage.morphology import binary_fill_holes,binary_dilation


class AStarAlgorithm(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("contrastBrightnessEditor_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)
            self.as_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=parent)

            thicknessLabelUnion = Qt.QLabel('Union thickness')
            self.thicknessSliderUnion = Qt.QSlider(QtCore.Qt.Horizontal)
            self.thicknessSliderUnion.setMinimum(0)
            self.thicknessSliderUnion.setMaximum(20)
            self.thicknessSliderUnion.setTickInterval(1)
            self.thicknessSliderUnion.setTickPosition(Qt.QSlider.TicksBelow)
            thicknessHLayoutUnion = QtWidgets.QHBoxLayout()
            thicknessHLayoutUnion.addWidget(thicknessLabelUnion)
            thicknessHLayoutUnion.addWidget(self.thicknessSliderUnion)
            self.thicknessSliderUnion.setEnabled(False)

            # medianMask - 3 tuple of ints
            medianMaskXLabel = Qt.QLabel('Median mask X: ')
            self.mmX = Qt.QLineEdit('8')
            medianMaskYLabel = Qt.QLabel('Median mask Y: ')
            self.mmY = Qt.QLineEdit('8')
            medianMaskZLabel = Qt.QLabel('Median mask Z: ')
            self.mmZ = Qt.QLineEdit('2')
            mmLayout = Qt.QHBoxLayout()
            mmLayout.addWidget(medianMaskZLabel)
            mmLayout.addWidget(self.mmZ)
            mmLayout.addWidget(medianMaskXLabel)
            mmLayout.addWidget(self.mmX)
            mmLayout.addWidget(medianMaskYLabel)
            mmLayout.addWidget(self.mmY)


            # minRadius - 3 tuple of ints
            minRadiusZLabel = Qt.QLabel('Min radius Z: ')
            self.minrZ = Qt.QLineEdit('0')
            minRadiusXLabel = Qt.QLabel('Min radius X: ')
            self.minrX = Qt.QLineEdit('1')
            minRadiusYLabel = Qt.QLabel('Min radius Y: ')
            self.minrY = Qt.QLineEdit('1')
            minrLayout = Qt.QHBoxLayout()
            minrLayout.addWidget(minRadiusZLabel)
            minrLayout.addWidget(self.minrZ)
            minrLayout.addWidget(minRadiusXLabel)
            minrLayout.addWidget(self.minrX)
            minrLayout.addWidget(minRadiusYLabel)
            minrLayout.addWidget(self.minrY)


            # maxRadius - 3 tuple of ints
            maxRadiusZLabel = Qt.QLabel('Max radius Z: ')
            self.maxrZ = Qt.QLineEdit('2')
            maxRadiusXLabel = Qt.QLabel('Max radius X: ')
            self.maxrX = Qt.QLineEdit('6')
            maxRadiusYLabel = Qt.QLabel('Max radius Y: ')
            self.maxrY = Qt.QLineEdit('6')
            maxrLayout = Qt.QHBoxLayout()
            maxrLayout.addWidget(maxRadiusZLabel)
            maxrLayout.addWidget(self.maxrZ)
            maxrLayout.addWidget(maxRadiusXLabel)
            maxrLayout.addWidget(self.maxrX)
            maxrLayout.addWidget(maxRadiusYLabel)
            maxrLayout.addWidget(self.maxrY)


            self.joinButton = Qt.QPushButton('Join elements')
            # explanationLabel = Qt.QLabel(
            #     'Please, be aware of having the corresponding raw image selected before joining the elements')
            self.applyChangesButton= Qt.QPushButton('Apply changes')
            self.applyChangesButton.setEnabled(False)

            self.as_layout.addLayout(mmLayout)
            self.as_layout.addLayout(minrLayout)
            self.as_layout.addLayout(maxrLayout)
            self.as_layout.addWidget(self.joinButton)
            self.as_layout.addLayout(thicknessHLayoutUnion)
            self.as_layout.addWidget(self.applyChangesButton)

    def __init__(self, viewer, segViewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = AStarAlgorithm._UI(parent=self)
        self.segViewer= segViewer
        self._viewer = viewer
        self._ui.joinButton.clicked.connect(self.joinElements)
        self._ui.thicknessSliderUnion.valueChanged.connect(self.growPath)
        self._ui.applyChangesButton.clicked.connect(self.openChangeLabelDialog)
        self._smUI = scm.SceneManagerUI()

    def openChangeLabelDialog(self):
        self._ui.thicknessSliderUnion.setEnabled(False)
        self._ui.applyChangesButton.setEnabled(False)
        self._viewer.chooseLabelButton()

    def joinElements(self):
        mn, mx = getAABBImg(self.segViewer.img == 3)
        self.slices = idxAABB(mn, mx)
        self.subLabelImg = self.segViewer.img[self.slices]
        selection = (self.subLabelImg == 3)
        labeled, ncomponents = self._viewer.getConnectedElements(selection)

        if ncomponents < 2:
            self._mw.warningMsg('Elements are already connected')
            return
        else:
            node = self._viewer.rawImg
            img = node.img
            self.subImg = img[self.slices].astype(np.float)
            self.subImg /= self.subImg.max()
            self._ui.thicknessSliderUnion.setEnabled(True)
            self._ui.applyChangesButton.setEnabled(True)
            self._mw.processDialog(
                lambda: self.computeAStar(labeled), False,
                title='',
                closeOnFinished=True, hideConsole=True)


    def computeAStar(self, labeled):
        labeled_aux = np.copy(labeled)
        nonZero = [np.count_nonzero(labeled_aux == i) for i in range(1, 3)]
        order = np.argsort(nonZero)[::-1]
        order += np.ones(order.shape, dtype=np.int)
        print(order)
        if order[0] == 1:  # si hay más pixeles de 1 que de 2
            labeled[(labeled_aux == 2)] = 1
            labeled[(labeled_aux == 1)] = 2
        print(labeled)

        def cost(idx1, idx2):
            return (1 - self.subImg[idx2]) * 100

        aStarImg = find_boundaries(self.subLabelImg, connectivity=3, mode='inner').astype(np.uint8)
        aStarImg = np.multiply(aStarImg, 3)
        aStarImg[(labeled == 1) & (aStarImg != 0)] = 1
        aStarImg[(labeled == 2) & (aStarImg != 0)] = 2

        self.p, os, cs = labeledImgAStar(aStarImg, hFunc='distanceField', costFunc=cost, retDebugInfo=True)
        x, y, z = zip(*self.p)
        self.subLabelImg[x, y, z] = 4
        self.growPath()
        

    def growPath(self):
        res = np.any(self.segViewer.img == 3)  # coges la selección
        if res:
            minRadius = np.array((int(self._ui.minrZ.text()), int(self._ui.minrY.text()), int(self._ui.minrX.text())))
            maxRadius = np.array((int(self._ui.maxrZ.text()), int(self._ui.maxrY.text()), int(self._ui.maxrX.text())))
            subImgUI = (self.subImg * np.iinfo(np.uint16).max).astype(np.uint16)
            mImg = median_filter(subImgUI, size=(int(self._ui.mmZ.text()), int(self._ui.mmY.text()), int(self._ui.mmX.text())))
            mImgCut = np.copy(mImg)
            mImgCut[(self.subLabelImg != 0) & (self.subLabelImg != 4)] = 0
            subImgBool = (self.subLabelImg==4)
            minStruct = ellipStruct(minRadius)
            subMinImgBool = binary_dilation(subImgBool, structure= minStruct)
            maxStruct = ellipStruct(maxRadius)
            subMaxImgBool = binary_dilation(subImgBool, structure=maxStruct)
            #test = np.zeros(self.subImg.shape, dtype=np.bool)
            test = (subMinImgBool) & np.logical_not((self.subLabelImg != 0) & (self.subLabelImg != 4))
            for i in self.p:
                tol = mImg[i] * (self._ui.thicknessSliderUnion.value() / 100)
                test += flood(mImgCut, i, tolerance=tol) & (subMaxImgBool)
                #print(i, tol, mImg[i])

            print('Slices ', self.slices)
            test = test.astype(int) * 4
            aux_img = np.copy(self.segViewer.img)
            aux_img[self.slices] = np.clip(self.subLabelImg + test, None, 4)

            self._viewer.tableWidget.clearSelection()
            aux_img2 = np.copy(self._viewer.showArray)
            aux = np.where(aux_img == 4, 3, aux_img2)
            self.segViewer.img = aux
        else:
            self._mw.warningMsg("Join some disconnected elements!")
