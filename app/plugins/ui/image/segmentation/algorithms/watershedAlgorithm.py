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

from PyQt5 import Qt
import numpy as np
from app.plugins.utils.image.image import getAABBImg, idxAABB
from skimage.segmentation import find_boundaries, watershed, flood
from skimage.morphology import dilation
from scipy import ndimage as ndi
from app.core.ui import mainWindow as MW
from app.plugins.ui.image.segmentation.algorithms.selectionOptions import SelectionOptions as selectOpt
from skimage.transform import rescale, resize, downscale_local_mean

class WatershedAlgorithm(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("waterShed_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred, Qt.QSizePolicy.Preferred)

            self.ws_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight, parent=parent)

            vLayout1 = Qt.QVBoxLayout()
            self.markersButtonGroup = Qt.QButtonGroup(parent)
            self.noMarkersButton = Qt.QRadioButton('Without markers')
            self.noMarkersButton.setChecked(True)
            self.dendriteMarkersButton = Qt.QRadioButton('Choose markers dendrite')
            self.spine1MarkersButton = Qt.QRadioButton('Choose markers spine 1')
            self.spine2MarkersButton = Qt.QRadioButton('Choose markers spine 2')
            self.backgroundMarkersButton = Qt.QRadioButton('Choose background markers')
            self.markersButtonGroup.addButton(self.noMarkersButton, 0)
            self.markersButtonGroup.addButton(self.dendriteMarkersButton, 5)
            self.markersButtonGroup.addButton(self.spine1MarkersButton, 6)
            self.markersButtonGroup.addButton(self.spine2MarkersButton, 7)
            self.markersButtonGroup.addButton(self.backgroundMarkersButton, 8)
            vLayout1.addWidget(self.noMarkersButton)
            vLayout1.addWidget(self.dendriteMarkersButton)
            vLayout1.addWidget(self.spine1MarkersButton)
            vLayout1.addWidget(self.spine2MarkersButton)
            vLayout1.addWidget(self.backgroundMarkersButton)

            vLayout2 = Qt.QVBoxLayout()
            self.resetMarkersButton = Qt.QPushButton('Reset markers')
            self.watershedButton = Qt.QPushButton('Perform watershed')
            self.applyChangesButton = Qt.QPushButton('Apply changes')
            vLayout2.addWidget(self.resetMarkersButton)
            vLayout2.addWidget(self.watershedButton)
            vLayout2.addWidget(self.applyChangesButton)
            self.ws_layout.addLayout(vLayout1)
            self.ws_layout.addLayout(vLayout2)

    def __init__(self, viewer, segViewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = WatershedAlgorithm._UI(parent=self)
        self._viewer = viewer
        self.segViewer= segViewer
        self.slices = None
        self._ui.watershedButton.clicked.connect(self.performWatershed)
        self._ui.resetMarkersButton.clicked.connect(self.resetMarkers)
        self._ui.markersButtonGroup.buttonClicked.connect(lambda: self.markersState(self._ui.markersButtonGroup))
        self._ui.applyChangesButton.clicked.connect(self.applyChanges)

    def resizeImage(self, image):
        imageResized = resize(image, (int(round(image.shape[0]*3.72439)), image.shape[1], image.shape[2]), preserve_range=True)
        return imageResized

    def roundImgToValues(self, image, values):
        arr=image.flatten()
        for i in range(arr.size):
            minDist = 1000
            for val in values:
                if np.round(abs(arr[i] - val)) <= minDist:
                    minDist = np.round(abs(arr[i] - val))
                    newValue = val
            arr[i] = int(newValue)

        arr= arr.reshape(image.shape)
        return arr

    def applyChanges(self):
        if self.slices is not None:
            auxImg = np.copy(self._viewer.segmentationImg)
            auxImg[self.globalSelectionTuple] = self.segViewer.img[self.globalSelectionTuple]
            self._viewer.updateWatershed(auxImg[self.slices], self.slices)
        self.slices=None

    def markersState(self, b):
        self._idChecked = b.checkedId()
        self._viewer.markersId = self._idChecked

    def resetMarkers(self):
        subSection = np.where(self.segViewer.img == self._idChecked)
        auxImg = np.copy(self.segViewer.img)
        auxImg[subSection] = 3
        self.segViewer.img = auxImg

    def performWatershed(self):
        res = np.any(self.segViewer.img == 3)
        if res:
            self._mw.processDialog(
                lambda: self.performWSProcess(), False,
                title='',
                closeOnFinished=True, hideConsole=True)
        else:
            self._mw.warningMsg('Nothing selected')

    def performWSProcessSpacing(self):
        selectedImg = (self.segViewer.img >= 3)
        mn, mx = getAABBImg(selectedImg)
        self.slices = idxAABB(mn, mx)
        selectedImg= selectedImg[self.slices]
        img= self.segViewer.img[self.slices]
        imgDendrite = (img == 5)
        imgSpine1 = (img == 6)
        imgSpine2 = (img == 7)
        imgBackground = (img == 8)

        #distance = ndi.distance_transform_edt(selectedImg)
        #distance = ndi.distance_transform_edt(selectedImg, sampling=[3.72439, 1, 1])
        distance = ndi.distance_transform_edt(selectedImg, sampling=[0.279911, 0.0751562, 0.0751562])
        markers = np.zeros((selectedImg.shape))
        markers[imgDendrite] = 1
        markers[imgSpine1] = 2
        markers[imgBackground] = 0
        markers[imgSpine2] = 4

        if np.any(markers):
            labels = watershed(-distance, markers, mask=selectedImg)
        else:
            labels = watershed(-distance, mask=selectedImg)

        aux_img = np.copy(self.segViewer.img)
        self.globalSelectionTuple = np.where(self.segViewer.img >= 3)
        tuple0 = self.globalSelectionTuple[0] - self.slices[0].start
        tuple1 = self.globalSelectionTuple[1] - self.slices[1].start
        tuple2 = self.globalSelectionTuple[2] - self.slices[2].start
        localSelectionTuple = (tuple0, tuple1, tuple2)
        aux_img[self.globalSelectionTuple] = labels[localSelectionTuple]
        #aux_img[self.globalSelectionTuple]= distance[localSelectionTuple]
        self.segViewer.img = aux_img

    def performWSProcess(self):
        selectedImg = (self.segViewer.img >= 3)
        mn, mx = getAABBImg(selectedImg)
        self.slices = idxAABB(mn, mx)

        selectedImgResized = self.resizeImage(selectedImg[self.slices])
        img = np.multiply(np.copy(self.segViewer.img), selectedImg)
        img[img==1]=0
        img[img==2]=0
        img[img==3]=0
        imgDendrite= (img==5)
        imgSpine1 = (img==6)
        imgSpine2= (img==7)
        imgBackground = (img==8)
        imgDendriteResized = self.resizeImage(imgDendrite[self.slices])
        imgDendriteResized = self.roundImgToValues(imgDendriteResized, [0,1])
        imgSpine1Resized = self.resizeImage(imgSpine1[self.slices])
        imgSpine1Resized = self.roundImgToValues(imgSpine1Resized, [0, 1])
        imgSpine2Resized = self.resizeImage(imgSpine2[self.slices])
        imgSpine2Resized = self.roundImgToValues(imgSpine2Resized, [0, 1])
        imgBckgResized = self.resizeImage(imgBackground[self.slices])
        imgBckgResized = self.roundImgToValues(imgBckgResized, [0, 1])

        # imgNodeImgResized = self.resizeImage(img[self.slices])
        # imgNodeImgResized = self.roundImgToValues(imgNodeImgResized, np.unique(img[self.slices]))
        # imgDendrite = (imgNodeImgResized == 5)
        # imgSpine1 =(imgNodeImgResized == 6)
        # imgSpine2 = (imgNodeImgResized == 7)
        # imgBackground = (imgNodeImgResized == 8)

        distance = ndi.distance_transform_edt(selectedImgResized)
        markers = np.zeros((selectedImgResized.shape))
        markers[np.where(imgDendriteResized)] = 1
        markers[np.where(imgSpine1Resized)] = 2
        markers[np.where(imgSpine2Resized)] = 4
        markers[np.where(imgBckgResized)] = 0

        if np.any(markers):
            labels = watershed(-distance, markers, mask=selectedImgResized)
        else:
            labels = watershed(-distance, mask=selectedImgResized)

        labelsOldZ = resize(labels, (self.segViewer.img[self.slices].shape[0], labels.shape[1], labels.shape[2]))
        labelsOldZ *=labels.max()/labelsOldZ.max() #devolver al rango original
        labelsOldZ = self.roundImgToValues(labelsOldZ, np.unique(labels)) #redondear a las etiquetas
        aux_img = np.copy(self.segViewer.img)
        self.globalSelectionTuple = np.where(selectedImg)
        tuple0 = self.globalSelectionTuple[0] - self.slices[0].start
        tuple1 = self.globalSelectionTuple[1] - self.slices[1].start
        tuple2 = self.globalSelectionTuple[2] - self.slices[2].start
        localSelectionTuple = (tuple0, tuple1, tuple2)
        aux_img[self.globalSelectionTuple] = labelsOldZ[localSelectionTuple]
        self.segViewer.img = aux_img
