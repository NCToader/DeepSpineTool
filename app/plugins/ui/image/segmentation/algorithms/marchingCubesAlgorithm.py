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
from skimage.measure import mesh_surface_area
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from app.core.ui import mainWindow as MW
from app.core.model import scene as SC
from skimage import measure
from app.plugins.model.meshNode.meshNode import MeshNode
from app.plugins.utils.image.image import getAABBImg, idxAABB
from app.plugins.model.folder.folder import Folder
from app.plugins.model.tableNode.tableNode import TableNode
import math

class MarchingCubesAlgorithm(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("marchingCubes_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred, Qt.QSizePolicy.Preferred)
            self.ws_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=parent)
            # spacinglength - 3 tuple of floats
            spacingXLabel = Qt.QLabel('Spacing X')
            self.lineSpacingX = Qt.QLineEdit('0.0751562')
            spacingYLabel = Qt.QLabel('Spacing Y')
            self.lineSpacingY = Qt.QLineEdit('0.0751562')
            spacingZLabel = Qt.QLabel('Spacing Z')
            self.lineSpacingZ = Qt.QLineEdit('0.279911')
            spacingLayout = Qt.QHBoxLayout()
            spacingLayout.addWidget(spacingXLabel)
            spacingLayout.addWidget(self.lineSpacingX)
            spacingLayout.addWidget(spacingYLabel)
            spacingLayout.addWidget(self.lineSpacingY)
            spacingLayout.addWidget(spacingZLabel)
            spacingLayout.addWidget(self.lineSpacingZ)
            prefixLayout = Qt.QHBoxLayout()
            prefixLabel = Qt.QLabel('Prefix: ')
            self.prefixLineEdit = Qt.QLineEdit()
            prefixLayout.addWidget(prefixLabel)
            prefixLayout.addWidget(self.prefixLineEdit)

            # correctionFactor - 3 tuple of floats
            cfXLabel = Qt.QLabel('Correction factor X:')
            self.correctionFactorX = Qt.QLineEdit('1.0')
            cfYLabel = Qt.QLabel('Correction factor Y:')
            self.correctionFactorY = Qt.QLineEdit('1.0')
            cfZLabel = Qt.QLabel('Correction factor Z:')
            self.correctionFactorZ = Qt.QLineEdit('1.0')
            cfLayout = Qt.QHBoxLayout()
            cfLayout.addWidget(cfXLabel)
            cfLayout.addWidget(self.correctionFactorX)
            cfLayout.addWidget(cfYLabel)
            cfLayout.addWidget(self.correctionFactorY)
            cfLayout.addWidget(cfZLabel)
            cfLayout.addWidget(self.correctionFactorZ)

            self.mcButton = Qt.QPushButton('Perform marching cubes')
            self.ws_layout.addLayout(spacingLayout)
            self.ws_layout.addLayout(prefixLayout)
            self.ws_layout.addLayout(cfLayout)
            self.ws_layout.addWidget(self.mcButton)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = MarchingCubesAlgorithm._UI(parent=self)
        self._viewer = viewer
        self._ui.mcButton.clicked.connect(self.performMarchingCubes)

    def computeMeshArea(self, verts, faces, row):
        area = mesh_surface_area(verts, faces)
        area = '{:06}'.format(area)
        self._viewer.tableWidget.setItem(row, 5, QTableWidgetItem(str(area)))
        return area

    def performMarchingCubes(self):
        self._mw.processDialog(
            self.processMC, False,
            title='Processing marching cubes',
            closeOnFinished=True, hideConsole=True)

    def processMC(self):
        usingBB = True
        if usingBB:
            mn, mx = getAABBImg(self._viewer.segmentationImg)
            self.slices = idxAABB(mn, mx)
            imgSizeY= self._viewer.segmentationImg.shape[1]
        spinesDict = []
        folderNode = Folder(name='3D Models')
        SC.Scene().addNode2Parent(folderNode, parent=self._viewer.viewer._imageNode)
        row = 0
        prefix = str(self._ui.prefixLineEdit.text())
        if usingBB:
            dendriteArray = self._viewer.labelsList[0]['label_array'][self.slices]
        else:
            dendriteArray = self._viewer.labelsList[0]['label_array']
        self._spacing = (
        float(self._ui.lineSpacingX.text()), float(self._ui.lineSpacingY.text()), float(self._ui.lineSpacingZ.text()))
        for label in range(0, 2):
            if usingBB:
                elementsArray = self._viewer.labelsList[label]['elements_array'][self.slices]
            else:
                elementsArray = self._viewer.labelsList[label]['elements_array']
            values = np.unique(elementsArray)
            if label == 0:
                strLabel = 'Dendrite'
                name = '{}_{}'.format(prefix, strLabel)
                if usingBB:
                    verts, faces, normals = self.performMC(dendriteArray, mn, mx, imgSizeY)
                else:
                    verts, faces, normals = self.performMC(dendriteArray)
                self.addMeshNode(name, verts, faces, normals, folderNode)
            elif label == 1:
                strLabel = 'Spine'
            for value in values[values != 0]:
                name = '{}_{}_{:04}'.format(prefix, strLabel, value)
                _image = (elementsArray == value)
                if usingBB:
                    verts, faces, normals = self.performMC(_image, mn, mx, imgSizeY)
                else:
                    verts, faces, normals = self.performMC(_image)
                area = self.computeMeshArea(verts, faces, row)
                if label == 1:
                    self.addMeshNode(name, verts, faces, normals, folderNode)
                    spineElement = {
                        'volume': np.count_nonzero(_image)*self._spacing[0]*self._spacing[1]*self._spacing[2],
                        'area': area
                    }
                    spinesDict.append(spineElement)
                row += 1
        tableNode = TableNode(name = 'Spines Data', spinesDict = spinesDict)
        SC.Scene().addNode2Parent(tableNode, parent=self._viewer.viewer._imageNode)

    def rotationMatrix(self, degrees):
        mat = np.array([[math.cos(degrees), -math.sin(degrees), 0, 0],
                        [math.sin(degrees), math.cos(degrees), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        return mat

    def performMC (self, image, bbMin=None, bbMax= None, imgSizeY = 1024):
        image = np.transpose(image, (2, 1, 0)) # x, y, z
        image = np.flip(image, 1)#x,-y,z
        verts, faces, normals, _ = measure.marching_cubes_lewiner(image, level=0.5, spacing=self._spacing)

        if bbMin is not None and bbMax is not None:
            bbOrigTransp= np.array([bbMin[2], imgSizeY-bbMax[1], bbMin[0]])
            offset = bbOrigTransp * self._spacing
            for i in range(len(verts)):
                verts[i]= verts[i] + offset
        return verts, faces, normals

    def addMeshNode(self, name, verts, faces, normals, parentNode):
        node = MeshNode(name=name, indices=faces, vertices=verts, normals=normals)
        node.scale((float(self._ui.correctionFactorX.text()), float(self._ui.correctionFactorY.text()),
                    float(self._ui.correctionFactorZ.text())))
        SC.Scene().addNode2Parent(node, parent=parentNode)
