import time

from PyQt5 import Qt, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from scipy.ndimage.measurements import label

from app.core.ui import mainWindow as MW
from app.core.utils import SingletonDecorator
from app.plugins.model.image.image import Image
from app.plugins.ui import sceneManagerUi as scm
from app.plugins.ui.image.viewer.img3Viewer import Img3Viewer
from app.plugins.utils.image.colorMapUtils import createColorMap
from app.plugins.utils.image.image import getAABBImg, idxAABB
from app.plugins.ui.image.segmentation import algorithms
import numpy as np
from app.core.model import scene as SC
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
from app.plugins.ui.image.segmentation.customDialog import CustomDialog

import vtkmodules
print(vtkmodules.__file__)


class SegmentationManager(Qt.QWidget):

    def __init__(self, rawViewer, segViewer, elementsImageNode=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._mw = MW.MainWindow()
        self.viewer = segViewer
        self.rawImg = rawViewer._imageNode
        self.labelsList = []
        self.segmentationImg = np.zeros((self.viewer.img.shape))
        self.maskImg = np.full((self.segmentationImg.shape), True)
        self.maskElements = np.full((self.segmentationImg.shape), True)
        self.selection = np.full((self.segmentationImg.shape), False)
        self.current_selection = np.full((self.segmentationImg.shape), False)
        self.maskElementID = np.full((self.segmentationImg.shape), False)
        self.elementsImageNode = elementsImageNode
        self.thicknessValueXY = 1
        self.thicknessValueZ = 1
        self.keepElementBoundaries = True
        self.checkConnectedToDendrite = False
        self.diagonalsConnected = False
        self.markersId = 0
        self.createLabelsArrays(self.viewer.img)
        self.showArray = np.multiply(self.maskElements, self.segmentationImg)
        self.pltOptions()

        self.map = createColorMap('default', [(0.99, 0.99, 0.99), (0, 0.8, 0), (0, 0.5, 1), (1, 0, 0), (1, 0.29, 0.87),
                                               (0.29, 1, 0.06), (0.06, 1, 1), (1, 1, 0), (1, 1, 0.8)])
        self.viewer.renderer.setPlotParams(vmin=0, vmax=8, cmap=self.map)
        self.updateSpVisCmap()
        self.press = None
        self.viewer.renderer._fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.viewer.renderer._fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        self.viewer.renderer._fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.viewer.renderer._fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.viewer.renderer._fig.canvas.mpl_connect('scroll_event', self.onscroll)
        self.oneClickTrigger = False
        self.timeFirstClick = 0
        self.rs = RectangleSelector(self.viewer.renderer.ax, self.onselect, drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels', interactive=True)
        self.spVis=False


    def updateSpVisCmap(self):
        Ncolors = np.count_nonzero(self.labelsList[1]['elements_array']) + 2
        colorList = []
        colorList.append((0.99, 0.99, 0.99))
        colorList.append((0, 0.8, 0))
        for i in range(Ncolors):
            colorList.append(np.random.rand(3, ))

        self.spVisCmap = createColorMap('spVis', colorList)

    def keyPressEvent(self, event):
        print('Qt key event ', event.text())

    def onpress(self, event):
        if event.key == 'ctrl+d':
            self.resetSelection()
        elif event.key == 'pagedown':
            self.viewer.renderer.sliceIdx = self.viewer.renderer.sliceIdx + 1
        elif event.key == 'pageup':
            self.viewer.renderer.sliceIdx = self.viewer.renderer.sliceIdx - 1
        elif event.key == 'ctrl+v':
            self.spVis=True
            print('Visualization changed')
            _xlimAux = self.viewer.renderer.xlim
            _ylimAux = self.viewer.renderer.ylim
            #cambiar la visualización al array de elementos más el array de dendritas y crear un nuevo mapa de color acorde a estos nuevos elementos
            self.viewer.img = np.add(self.labelsList[0]['label_array'], self.labelsList[1]['elements_array'])
            self.viewer.renderer.setPlotParams(cmap=self.spVisCmap)
            self.viewer.renderer.xlim = _xlimAux
            self.viewer.renderer.ylim = _ylimAux


    def onscroll(self, event):
        if event.step>0:
            self.viewer.renderer.sliceIdx = self.viewer.renderer.sliceIdx + 1
        elif event.step<0:
            self.viewer.renderer.sliceIdx = self.viewer.renderer.sliceIdx - 1


    def selectRow(self, row):
        self.tableWidget.selectRow(row)

    def resetVisualization(self):
        _xlimAux = self.viewer.renderer.xlim
        _ylimAux = self.viewer.renderer.ylim
        self.viewer.renderer.setPlotParams(vmin=0, vmax=8, cmap=self.map)
        self.updateRender()
        self.viewer.renderer.xlim = _xlimAux
        self.viewer.renderer.ylim = _ylimAux

    def getRow(self, _id, _label):
        items = self.tableWidget.findItems(str(_id), QtCore.Qt.MatchExactly)
        row=None
        if items:
            for item in items:
                if self.tableWidget.cellWidget(item.row(), 1).currentIndex() == _label:
                    row = item.row()
        return row

    def getSelectionLabelAndId(self, _x, _y, _z):
        selectionId=-1
        if self.viewer.renderer.showMaximumProjection:
            selectionLabel = int((self.viewer.img[:, _y, _x]).max() - 1)
        else:
            selectionLabel = int(self.viewer.img[_z, _y, _x] - 1)
        if selectionLabel == 0 or selectionLabel == 1:
            if self.viewer.renderer.showMaximumProjection:
                selectionId = (self.labelsList[selectionLabel]['elements_array'][:, _y, _x]).max()
            else:
                selectionId = self.labelsList[selectionLabel]['elements_array'][_z, _y, _x]
        return selectionLabel, selectionId

    def onselect(self, eclick, erelease):
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        print(self.selection)
        print(self.rs.extents)
        if self.spVis:
            self.resetVisualization()
            self.spVis = False
        self.init_coord = eclick
        self.end_coord = erelease
        minY = np.clip(int(np.floor(self.rs.extents[2])), 0, self.viewer.img.shape[1])
        maxY = np.clip(int(np.ceil(self.rs.extents[3])), 0, self.viewer.img.shape[1])
        minX = np.clip(int(np.floor(self.rs.extents[0])), 0, self.viewer.img.shape[2])
        maxX = np.clip(int(np.ceil(self.rs.extents[1])), 0, self.viewer.img.shape[2])
        if self.viewer.renderer.showMaximumProjection:
            minZ = 0
            maxZ = self.viewer.img.shape[0]
        else:
            minZ = self.viewer.renderer.sliceIdx
            maxZ = minZ +1
        slices = (slice(minZ, maxZ, None), slice(minY, maxY, None), slice(minX, maxX, None))
        _x = int((maxX+minX)/2)
        _y = int((maxY+minY)/2)
        _z = int((maxZ+minZ)/2)
        selectionLabel, selectionId = self.getSelectionLabelAndId(_x, _y, _z)
        print('Selection from: ', minX, ' to ', maxX, ' and from ', minY, ' to ', maxY)
        print(_x, _y, _z)
        print(selectionLabel, selectionId)
        if selectionLabel >= 0 and self.keepElementBoundaries:
            if (not np.any(self.selection)):
                self.maskElementID = (self.labelsList[selectionLabel]['elements_array'] == selectionId)
        aux_img = np.copy(self.viewer.img)
        self.selection[slices]=True
        if self.keepElementBoundaries:
            self.selection = np.logical_and(self.selection, self.maskElementID)
        aux_img[self.selection] = 3
        self.viewer.img = aux_img

    def onclick(self, event):
        if self.spVis:
            self.resetVisualization()
            self.spVis = False
        _x = int(round(event.xdata))
        _y = int(round(event.ydata))
        _z = self.viewer.renderer.sliceIdx
        selectionLabel, selectionId = self.getSelectionLabelAndId(_x,_y, _z)
        if selectionLabel >= 0 and self.keepElementBoundaries:
            if (not np.any(self.selection)):
                self.maskElementID = (self.labelsList[selectionLabel]['elements_array'] == selectionId)

        if event.button == 1:  # seleccionar objeto entero
            if selectionId >= 0:  # buscas la row de acuerdo al id y al label
                self.selectRow(self.getRow(selectionId, selectionLabel))
            if selectionLabel >= 0 and selectionLabel<2 and self.keepElementBoundaries:
                self.maskElementID = (self.labelsList[selectionLabel]['elements_array'] == selectionId)
            if self.oneClickTrigger == False:
                self.oneClickTrigger = True
                self.timeFirstClick = time.time()
            else:
                doubleClickInterval = time.time() - self.timeFirstClick
                if doubleClickInterval < 0.5:
                    self.zoomToData(self.selection)
                self.oneClickTrigger = False
                self.timeFirstClick = 0

        if event.button == 2:  # selección personalizada
            if self.viewer.renderer.showMaximumProjection:
                if self.markersId == 0:
                    self.selection[:, _y:_y + self.thicknessValueXY, _x:_x + self.thicknessValueXY] = not (
                        np.all(self.selection[:, _y:_y + self.thicknessValueXY, _x:_x + self.thicknessValueXY]))
                self.current_selection[:, _y:_y + self.thicknessValueXY, _x:_x + self.thicknessValueXY] = True
            else:
                if self.markersId == 0:
                    self.selection[_z:_z + self.thicknessValueZ, _y:_y + self.thicknessValueXY,
                    _x:_x + self.thicknessValueXY] = not (np.all(self.selection[_z:_z + self.thicknessValueZ,
                                                                 _y:_y + self.thicknessValueXY,
                                                                 _x:_x + self.thicknessValueXY]))
                self.current_selection[_z:_z + self.thicknessValueZ, _y:_y + self.thicknessValueXY,
                _x:_x + self.thicknessValueXY] = True
            if self.keepElementBoundaries:
                self.selection = np.logical_and(self.selection, self.maskElementID)
            self.aux_img = np.copy(self.viewer.img)
            selectionValue = 3
            if self.markersId > 0:
                selectionValue = self.markersId
            self.aux_img[self.current_selection] = selectionValue  # en los pixeles de la selección actual se pone el número correspondiente
            self.aux_img[self.selection == False] = self.showArray[self.selection == False]  # donde no hay selección se pinta el array normal
            self.viewer.img = self.aux_img
            self.press = event.x, event.y, event.xdata, event.ydata
            self.current_selection = np.full((self.segmentationImg.shape), False)  # se resetea la selección actual


    def onrelease(self, event):
        self.press = None

    def onmotion(self, event):
        if self.press is None: return
        _x = int(round(event.xdata))
        _y = int(round(event.ydata))
        _z = self.viewer.renderer.sliceIdx
        if self.viewer.renderer.showMaximumProjection:
            self.current_selection[:, _y:_y + self.thicknessValueXY, _x:_x + self.thicknessValueXY] = True
            if self.markersId == 0:
                self.selection[:, _y:_y + self.thicknessValueXY, _x:_x + self.thicknessValueXY] = True
        else:
            self.current_selection[_z:_z + self.thicknessValueZ, _y:_y + self.thicknessValueXY,
            _x:_x + self.thicknessValueXY] = True
            if self.markersId == 0:
                self.selection[_z:_z + self.thicknessValueZ, _y:_y + self.thicknessValueXY,
                _x:_x + self.thicknessValueXY] = True
        if self.keepElementBoundaries:
            self.selection = np.logical_and(self.selection, self.maskElementID)
        selectionValue = 3
        if self.markersId > 0:
            selectionValue = self.markersId
        self.aux_img[self.current_selection] = selectionValue
        self.aux_img[self.selection == False] = self.showArray[self.selection == False]  # donde no hay selección se pinta el array normal
        self.viewer.img = self.aux_img
        self.current_selection = np.full((self.segmentationImg.shape), False)

    def fillTable(self):
        self.tableWidget.setRowCount(0)
        nLabel0 = np.unique(self.labelsList[0]['elements_array']).size - 1
        print('Nº de dendritas ', nLabel0)
        nLabel1 = np.unique(self.labelsList[1]['elements_array']).size - 1
        print('Nº de espinas ', nLabel1)
        self.tableWidget.setRowCount(nLabel0 + nLabel1)
        self.cmbs = [None]*(nLabel0 + nLabel1)*2
        self.cb_list = [None] * (nLabel0+nLabel1)*2
        rowCount = 0
        count =1
        auxLabelsList0= np.copy(self.labelsList[0]['elements_array'])
        auxLabelsList1 = np.copy(self.labelsList[1]['elements_array'])
        for i in self.removeZeroValues(np.unique(self.labelsList[0]['elements_array'])):
            auxLabelsList0[auxLabelsList0==i]=count
            count+=1
        for i in self.removeZeroValues(np.unique(self.labelsList[1]['elements_array'])):
            auxLabelsList1[auxLabelsList1==i]=count
            count+=1
        self.labelsList[0]['elements_array'] = auxLabelsList0
        self.labelsList[1]['elements_array'] = auxLabelsList1
        for id in self.removeZeroValues(np.unique(self.labelsList[0]['elements_array'])):
            cmb = Qt.QComboBox()
            cmb.addItem("Dendrite")
            cmb.addItem("Spine")
            self.cmbs[id]=cmb
            showCheckbox = Qt.QCheckBox()
            showCheckbox.setChecked(True)
            self.cb_list[id]=showCheckbox

        for id in self.removeZeroValues(np.unique(self.labelsList[1]['elements_array'])):
            cmb = Qt.QComboBox()
            cmb.addItem("Dendrite")
            cmb.addItem("Spine")
            self.cmbs[id]=cmb
            showCheckbox = Qt.QCheckBox()
            showCheckbox.setChecked(True)
            self.cb_list[id]=showCheckbox

        # dendritas
        for i in self.removeZeroValues(np.unique(self.labelsList[0]['elements_array'])):
            # id item
            id_item = QTableWidgetItem(str(i))
            id_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(id_item))
            # comboBox Label item
            self.cmbs[i].currentIndexChanged.connect(lambda _, i=i: self.chooseLabelComboBox(self.cmbs[i], i))
            self.tableWidget.setCellWidget(rowCount, 1, self.cmbs[i])
            # checkBox show Element item
            self.cb_list[i].stateChanged.connect(
                lambda checked, i=i: self.showElements(self.cb_list[i], 1, i))
            self.tableWidget.setCellWidget(rowCount, 2, self.cb_list[i])
            # pixelCount item
            pixelCount = np.count_nonzero(self.labelsList[0]['elements_array'] == i)
            pixelCount = '{:06}'.format(pixelCount)
            pixelCountItem = QTableWidgetItem(str(pixelCount))
            pixelCountItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowCount, 3, QTableWidgetItem(pixelCountItem))
            rowCount+=1
        # espinas
        for i in self.removeZeroValues(np.unique(self.labelsList[1]['elements_array'])):
            # id item
            id_item = QTableWidgetItem(str(i))
            id_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(id_item))
            # comboBox Label item
            self.cmbs[i].setCurrentIndex(1)
            self.cmbs[i].currentIndexChanged.connect(
                lambda _, i=i: self.chooseLabelComboBox(self.cmbs[i], i))
            self.tableWidget.setCellWidget(rowCount, 1, self.cmbs[i])
            # checkBox show Element item
            self.cb_list[i].stateChanged.connect(
                lambda checked,i=i: self.showElements(self.cb_list[i], 2, i))
            self.tableWidget.setCellWidget(rowCount, 2, self.cb_list[i])
            # pixelCount item
            pixelCount = np.count_nonzero(self.labelsList[1]['elements_array'] == i)
            pixelCount = '{:06}'.format(pixelCount)
            pixelCountItem = QTableWidgetItem(str(pixelCount))
            pixelCountItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowCount, 3, QTableWidgetItem(pixelCountItem))
            if self.checkConnectedToDendrite:
                aux_string = self.isConnectedToDendrite(i )
                self.tableWidget.setItem(rowCount, 4, QTableWidgetItem(aux_string))
            rowCount+=1

    def isConnectedToDendrite(self, spine_id):
        aux_array = np.copy(self.labelsList[0]['elements_array'])
        _, ndendrites = self.getConnectedElements(aux_array, self.diagonalsConnected)
        aux_array[self.labelsList[1]['elements_array'] == spine_id] = 1  # le añades al array de dendritas los pixeles donde se encuentra esta espina
        labeled, ncomponents = self.getConnectedElements(aux_array, self.diagonalsConnected)
        if ncomponents > ndendrites:
            aux_string = 'Disconnected'
        else:
            aux_string = 'Connected'
        return aux_string

    def pltOptions(self):
        vLayout1 = QtWidgets.QVBoxLayout()
        vLayout2 = QtWidgets.QVBoxLayout()
        hLayout1 = QtWidgets.QHBoxLayout()
        vLayout3 = QtWidgets.QVBoxLayout()
        self.labelCheckboxes0 = Qt.QCheckBox('Show all dendrites')
        self.labelCheckboxes0.setChecked(True)
        self.labelCheckboxes1 = Qt.QCheckBox('Show all spines')
        self.labelCheckboxes1.setChecked(True)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Type', 'Show element', 'Pixel count', 'Connected to dendrite', 'Area'])
        self.tableWidget.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
        self.tableWidget.setSortingEnabled(True)
        self.fillTable()

        deleteButton = Qt.QPushButton('Delete selection')
        resetButton = Qt.QPushButton('Reset selection')
        vLayout1.addWidget(self.labelCheckboxes0)
        vLayout1.addWidget(self.labelCheckboxes1)

        changeLabelButton = Qt.QPushButton('Change label')

        vLayout2.addWidget(changeLabelButton)
        vLayout2.addWidget(resetButton)
        vLayout2.addWidget(deleteButton)
        hLayout1.addLayout(vLayout1)
        hLayout1.addLayout(vLayout2)
        # tabs
        modifiers_widget = Qt.QWidget()
        modifiers_widget.setSizePolicy(Qt.QSizePolicy.Preferred, Qt.QSizePolicy.Preferred)
        modifiers_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=modifiers_widget)

        modifiers_tabWidget = Qt.QTabWidget(parent=modifiers_widget)
        modifiers_tabWidget.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Fixed)
        modifiers_layout.addWidget(modifiers_tabWidget)
        modifiers_layout.addWidget(Qt.QWidget(parent=modifiers_widget))

        modifiers_tabWidget.addTab(algorithms.SelectionOptions(viewer=self), 'Selection options')
        modifiers_tabWidget.addTab(algorithms.WatershedAlgorithm(viewer=self, segViewer=self.viewer),
                                   'Split elements')
        modifiers_tabWidget.addTab(algorithms.AStarAlgorithm(viewer=self, segViewer=self.viewer), 'Join elements')
        modifiers_tabWidget.addTab(algorithms.TableOptions(viewer=self), 'Table options')
        modifiers_tabWidget.addTab(algorithms.MarchingCubesAlgorithm(viewer=self), 'Marching cubes')

        vLayout3.addLayout(hLayout1)
        vLayout3.addWidget(modifiers_widget)
        vLayout3.addWidget(self.tableWidget)

        self.setLayout(vLayout3)

        deleteButton.clicked.connect(self.removeSelection)
        resetButton.clicked.connect(self.resetSelection)
        changeLabelButton.clicked.connect(self.chooseLabelButton)
        self.labelCheckboxes0.stateChanged.connect(lambda: self.showLabel(self.labelCheckboxes0, 1))
        self.labelCheckboxes1.stateChanged.connect(lambda: self.showLabel(self.labelCheckboxes1, 2))
        self.tableWidget.itemSelectionChanged.connect(self.highlightItemData)
        self.tableWidget.cellDoubleClicked.connect(self.highlightAndZoomData)
        modifiers_tabWidget.currentChanged.connect(lambda: self.tabChanged(modifiers_tabWidget))

    def tabChanged(self, tabWidget):
        if (tabWidget.currentIndex() != 1):
            self.markersId=0

    def getNeighbourhoodIdValue(self, globalNewValuePosition, new_label):
        zMin = np.clip(globalNewValuePosition[0].min()-1, a_min=0, a_max=self.viewer.img.shape[0]-1)
        zMax = np.clip(globalNewValuePosition[0].max()+1, a_min=0, a_max=self.viewer.img.shape[0]-1)
        yMin = np.clip(globalNewValuePosition[1].min()-1, a_min=0, a_max=self.viewer.img.shape[1]-1)
        yMax = np.clip(globalNewValuePosition[1].max()+1, a_min=0, a_max=self.viewer.img.shape[1]-1)
        xMin = np.clip(globalNewValuePosition[2].min()-1, a_min=0, a_max=self.viewer.img.shape[2]-1)
        xMax = np.clip(globalNewValuePosition[2].max()+1, a_min=0, a_max=self.viewer.img.shape[2]-1)
        zArray = globalNewValuePosition[0]
        yArray = globalNewValuePosition[1]
        xArray = globalNewValuePosition[2]
        for _z in range(zMin, zMax+1):
            for _y in range(yMin, yMax+1):
                for _x in range(xMin, xMax+1):
                    zArray = np.append(zArray, _z)
                    yArray = np.append(yArray, _y)
                    xArray = np.append(xArray, _x)

        neighbourTuple = (zArray, yArray, xArray)
        _id = self.labelsList[new_label]['elements_array'][neighbourTuple]
        unique, count = np.unique(self.removeZeroValues(_id), return_counts=True)
        print ('Neighbours id ', unique)
        if unique.size > 0:
            temp = np.argsort(count)[::-1]
            return unique[temp]
        else:
            return unique

    def updatePixelCount(self, label, _id):
        row = self.getRow(_id, label)
        print('Updating pixels of row ', row)
        if row is not None:
            pixelCount = np.count_nonzero(self.labelsList[label]['elements_array'] == _id)
            print('Pixelcount ', pixelCount)
            if pixelCount == 0:
                self.tableWidget.removeRow(row)
            else:
                pixelCount = '{:06}'.format(pixelCount)
                pixelCountItem = QTableWidgetItem(str(pixelCount))
                pixelCountItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 3, QTableWidgetItem(pixelCountItem))

    def changeLabel(self, subImg,  new_label, indexChanged=False):
            mn, mx = getAABBImg(subImg)
            self.slices = idxAABB(mn, mx)
            auxImg = np.multiply(self.segmentationImg[self.slices], subImg[self.slices])
            old_ids = []
            if np.unique(self.removeZeroValues(auxImg)).size>0:
                if new_label ==0:
                    old_label=1
                else:
                    old_label = 0
            else: #asume que es fondo
                old_label =-1


            nAuxLabels, ncomponents = self.getConnectedElements(subImg[self.slices], self.diagonalsConnected)
            for component in range(1, ncomponents + 1):
                globalNewValuePosition = self.localToGlobal(np.where(nAuxLabels == component), self.slices)
                if old_label>=0:
                    old_ids = np.unique(self.labelsList[old_label]['elements_array'][globalNewValuePosition])
                    self.updateElementFromArrays(globalNewValuePosition, old_label, remove=True)
                if new_label == 2:
                    self.createItem(1, subImg)
                else:
                    # buscas en la posición que hay en el alrededor en el array de new label
                    _ids = self.getNeighbourhoodIdValue(globalNewValuePosition, new_label)
                    if _ids.size==0:
                        self.createItem(new_label, globalNewValuePosition)
                    else:
                        choosenID = _ids[0] #esto será así, si devolvemos la lista ordenada por orden de frecuencia
                        self.updateElementFromArrays(globalNewValuePosition, new_label, choosenID) #se le asigna el id al 'nuevo_elemento'
                        if _ids.size>1:
                            for _id in _ids[1:]:
                                idPosition = np.where(self.labelsList[new_label]['elements_array']==_id)
                                self.updateElementFromArrays(idPosition, new_label, choosenID)
                                self.updatePixelCount(new_label, _id)
                        self.updatePixelCount(new_label, choosenID)
                        self.updateRender()

                for old_id in old_ids:
                    if indexChanged:
                        old_label=new_label
                    self.updatePixelCount(old_label, old_id)

    def chooseLabelButton(self):
        selection = (self.viewer.img == 3)
        res = np.any(selection)
        if res:
            items = ('Dendrite', 'Spine', 'New spine')
            item, ok = Qt.QInputDialog.getItem(self, 'Label selection', 'Choose label', items, 0, False)
            if ok and item:
                new_label = items.index(item)
                self.changeLabel(selection, new_label)
        else:
            self._mw.warningMsg("Nothing selected")

    def resetSelectionAndRectangle(self):
        self.rs.set_active(False)
        self.resetSelection()
        self.rs.set_active(True)

    def resetSelection(self):
        self.selection = np.full((self.segmentationImg.shape), False)
        self.showArray = np.multiply(self.maskElements, self.segmentationImg)
        self.viewer.img = self.showArray
        self.tableWidget.clearSelection()

    def createItem(self, label, subArrayPosition):
        # los añadimos a los arrays de la nueva etiqueta
        new_id = np.max(self.labelsList[1]['elements_array']) + 1
        self.updateElementFromArrays(subArrayPosition, label, new_id)
        self.updateRender()

        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        # id item
        id_item = QTableWidgetItem(str(new_id))
        id_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(id_item))
        # comboBox Label item
        cmb = Qt.QComboBox()
        cmb.addItem("Dendrite")
        cmb.addItem("Spine")
        cmb.setCurrentIndex(label)
        self.cmbs[new_id] = cmb
        self.cmbs[new_id].currentIndexChanged.connect(lambda: self.chooseLabelComboBox(self.cmbs[new_id], new_id))
        self.tableWidget.setCellWidget(row, 1, self.cmbs[new_id])

        # checkBox show Element item
        aux_checkbox = Qt.QCheckBox()
        aux_checkbox.setChecked(True)
        self.cb_list[new_id] = aux_checkbox
        self.cb_list[new_id].stateChanged.connect(lambda: self.showElements(self.cb_list[new_id], label + 1, new_id))
        self.tableWidget.setCellWidget(row, 2, aux_checkbox)

        # pixelCount item
        pixelCount = np.count_nonzero(self.labelsList[label]['elements_array'][subArrayPosition]==new_id)
        pixelCount = '{:06}'.format(pixelCount)
        pixelCountItem = QTableWidgetItem(str(pixelCount))
        pixelCountItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(row, 3, QTableWidgetItem(pixelCountItem))

    def createLabelsArrays(self, img):
        changeOrder = False
        self.labelsList = []
        values = np.unique(img)
        values = values[values!=0]
        arr = (img==values[0])
        _, ncomponents0 = self.getConnectedElements(arr, self.diagonalsConnected)
        arr = (img == values[1])
        _, ncomponents1 = self.getConnectedElements(arr, self.diagonalsConnected)
        if ncomponents0 > ncomponents1: #la etiqueta con menos elementos va a asumir que son dendritas y con más, espinas
            changeOrder = True
        count = 1
        aux_img = np.zeros((self.segmentationImg.shape))
        if changeOrder:
            values = np.sort(values)[::-1]
        for val in values:
            arr = np.multiply((img == val), count)
            if self.elementsImageNode.img is not None:
                labelElements = np.multiply((img == val), self.elementsImageNode.img)
            else:
                labelElements, ncomponents = self.getConnectedElements(arr, self.diagonalsConnected)
                if (count==2):
                    maxId = np.max(self.labelsList[0]['elements_array'])
                    labelElements = labelElements + maxId
                    labelElements[labelElements == maxId] = 0
            # initialize checkbox list
            label = {
                'label_array': arr,
                'elements_array': labelElements
            }
            self.labelsList.append(label)
            count += 1
            aux_img = np.add(aux_img, arr)

        self.viewer.img = np.copy(aux_img)
        self.viewer._imageNode.img = np.copy(self.viewer.img)
        self.segmentationImg = aux_img
        self.showArray = np.multiply(self.maskElements, self.segmentationImg)
        if self.elementsImageNode.img is None:
            self.elementsImageNode.img = np.add(self.labelsList[0]['elements_array'],
                                                self.labelsList[1]['elements_array'])



    def zoomToData(self, img):
        _xlimAux = self.viewer.renderer.xlim
        _ylimAux = self.viewer.renderer.ylim
        self.viewer.renderer.xlim = _xlimAux
        self.viewer.renderer.ylim = _ylimAux

        if img is not None:
            mn, mx = getAABBImg(img)
            projPlane = self.viewer.renderer.projectionPlane
            axis = projPlane.value[0]
            self.viewer.renderer.sliceIdx = int((mn[axis] + mx[axis]) // 2)

            v = [True, True, True]
            v[axis] = False

            mn = np.array(mn)[v]
            mx = np.array(mx)[v]

            if not projPlane.value[1]:
                mn = mn[::-1]
                mx = mx[::-1]

            dx = np.clip(self.viewer.img.shape[1]//100, a_min = 1, a_max = None)
            dy = np.clip(self.viewer.img.shape[2]//100, a_min = 1, a_max = None)

            self.viewer.renderer.xlim= (mn[0] - dx, mx[0] + (dx-1.0))
            self.viewer.renderer.ylim = (mx[1] + (dy-1.0), mn[1] - dy)

    def highlightAndZoomData(self):
        self.highlightItemData(zoom=True)

    def highlightItemData(self, zoom = False):
        self.selection = np.full((self.segmentationImg.shape), False)
        if len(self.tableWidget.selectedItems()) == 0:  # quitar highlight cuando no hay ningún elemento seleccionado
            aux_img = np.copy(self.showArray)
            self.viewer.img = aux_img
            return
        aux_img = np.copy(self.showArray)
        if len(self.tableWidget.selectedItems()) > 0:
            rows = []
            for item in self.tableWidget.selectedItems():
                rows.append(item.row())
            for r in np.sort(np.unique(rows))[::-1]:
                label = int(self.tableWidget.cellWidget(r, 1).currentIndex())
                _id = int(self.tableWidget.item(r, 0).text())
                res = np.where(self.labelsList[label]['elements_array'] == _id)
                aux_img[res] = 3
                self.selection[res] = True
                self.viewer.img = aux_img
                if zoom:
                    if len(np.unique(rows)) == 1:
                        self.zoomToData(self.selection)

    def getConnectedElements(self, img, diagonals=False):
        if diagonals:
            # diagonales conectadas
            structure = np.ones((3, 3, 3), dtype=np.int)  # connection filter
        else:
            # diagonales desconectados
            structure = np.zeros((3, 3, 3))
            structure[:, 1:2, :] = np.ones((3, 1, 3))
            structure[:, :, 1:2] = np.ones((3, 3, 1))
        labeled, ncomponents = label(img, structure)

        return labeled, ncomponents

    def updateElementFromArrays(self, arrayPosition, label, _id=0, remove=False):
        if remove:
            self.labelsList[label]['label_array'][arrayPosition] = 0
        else:
            self.labelsList[label]['label_array'][arrayPosition] = label + 1
        self.labelsList[label]['elements_array'][arrayPosition] = _id
        self.updateSpVisCmap()
        self.updateImageNodes()

    def updateRender(self, img=None):

        if img is None:
            img = np.add(self.labelsList[0]['label_array'], self.labelsList[1]['label_array'])
        self.segmentationImg = img
        self.showArray = np.multiply(self.maskElements, self.segmentationImg)
        self.viewer.img = self.showArray

    def updateImageNodes(self):
        print('Guardando imagen de etiquetas')
        self.viewer._imageNode.img = np.add(self.labelsList[0]['label_array'], self.labelsList[1]['label_array'])
        print('Guardando imagen de elementos')
        self.elementsImageNode.img = np.add(self.labelsList[0]['elements_array'], self.labelsList[1]['elements_array'])

    def localToGlobal(self, tupleOfLocalPositions, globalSlices):
        globalPos = (tupleOfLocalPositions[0]+globalSlices[0].start,
                     tupleOfLocalPositions[1] + globalSlices[1].start,
                     tupleOfLocalPositions[2] + globalSlices[2].start)
        return globalPos

    def slicesToTuple(self, slices):
        array0=[]
        array1=[]
        array2=[]
        for i in range(slices[0].start, slices[0].stop):
            for j in range(slices[1].start, slices[1].stop):
                for k in range(slices[2].start, slices[2].stop):
                    array0.append(i)
                    array1.append(j)
                    array2.append(k)
        tuple = (np.array(array0), np.array(array1), np.array(array2))
        return tuple

    def removeZeroValues(self, array):
        array = array[array!=0]
        return array

    def updateWatershed(self, wsArray, wsArraySlices):
        values = self.removeZeroValues(np.unique(wsArray))
        for val in values:
            val=int(val)
            if val == 4:
                newSpinePosition = self.localToGlobal(np.where(wsArray==4), wsArraySlices)
                self.createItem(1, newSpinePosition)
            else:
                oldLabelRegion = np.copy(self.labelsList[val-1]['label_array'][wsArraySlices])
                newLabelRegion = np.multiply(wsArray, wsArray==val)
                diffArray = newLabelRegion - oldLabelRegion
                if np.any(diffArray<0):
                    globalRemoveValuePosition = self.localToGlobal(np.where(diffArray<0), wsArraySlices)
                    self.updateElementFromArrays(globalRemoveValuePosition,val-1, remove=True)
                if np.any(diffArray>0):
                    globalChangeValuePosition = self.localToGlobal(np.where(diffArray > 0), wsArraySlices)
                    auxImg = np.zeros(self.viewer.img.shape)
                    auxImg[globalChangeValuePosition]= True
                    self.changeLabel(auxImg, val-1)

    def updateLabels(self):
        self.createLabelsArrays(img=self.segmentationImg)
        self.fillTable()

    def removeSelection(self):
        res = np.any(self.viewer.img == 3)
        if res:
            ok = self._mw.confirmMsg('Are you sure you want to delete this element?')
            if ok:
                currentVis = np.multiply(self.maskElements, self.segmentationImg)
                aux = np.where(self.viewer.img == 3)
                indices = np.where(currentVis[aux] == 0)
                result = (np.delete(aux[0], indices), np.delete(aux[1], indices), np.delete(aux[2], indices))

                self.updateElementFromArrays(result, 0, remove=True)
                self.updateElementFromArrays(result, 1, remove=True)

                self.updateRender()
                if len(self.tableWidget.selectedItems()) > 0:
                    rows = []
                    for item in self.tableWidget.selectedItems():
                        rows.append(item.row())
                    for row in np.sort(np.unique(rows))[::-1]:
                        self.tableWidget.removeRow(row)

                self.resetSelection()
        else:
            self._mw.warningMsg("Nothing selected")

    def chooseLabelComboBox(self, cmb, row_):
        ok = self._mw.confirmMsg('Are you sure you want to re-label this element?')
        row = self.tableWidget.currentRow()
        if row == -1:
            row = row_
        if ok:
            _id = int(self.tableWidget.item(row, 0).text())
            new_label = cmb.currentIndex()
            if new_label == 0:
                old_label = 1
            elif new_label == 1:
                old_label = 0
            subImg =  (self.labelsList[old_label]['elements_array'] ==_id)
            self.changeLabel(subImg, new_label, indexChanged=True)

    def showElements(self, b, label, i):
        if b.isChecked():
            self.maskElements[self.labelsList[label - 1]['elements_array'] == i] = True
        else:
            self.maskElements[self.labelsList[label - 1]['elements_array'] == i] = False

        self.showArray = np.multiply(self.maskElements, self.segmentationImg)
        self.viewer.img = self.showArray

    def showLabel(self, b, label):
        for val in np.unique(self.labelsList[label - 1]['elements_array']):
            if val == 0:
                continue
            self.cb_list[val-1].setChecked(b.isChecked())



class SegmentationSplitter(Qt.QSplitter):
    def __init__(self, parent=None, rawImg=None, segImg=None, manager=None):
        Qt.QMainWindow.__init__(self, parent)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(rawImg)
        self.addWidget(segImg)
        self.addWidget(manager)


@SingletonDecorator
class SegmentationConnector:
    def __init__(self, menuPath=None):
        self._mw = MW.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Segmentation"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$%$2"
        self._name = "Segmentation editor"

        self._mw.addAction(self._name, prefix=self._prefix)
        self._mw.addActionCB(self._name,
                             self.selectPredictionImage,
                             prefix=self._prefix)
        self._mw.addAction2Menu(self._name,
                                menuPath=self._menuPath,
                                prefix=self._prefix)

    def addViewers(self, rawView, segView, editionImgNode = None):
        # #conectar las señales de uno a otro
        def sliceRawToSeg(): segView.renderer.sliceIdx = rawView.renderer.sliceIdx
        rawView.renderer.sliceUpdatedSignal.connect(sliceRawToSeg)
        def sliceSegToRaw(): rawView.renderer.sliceIdx = segView.renderer.sliceIdx
        segView.renderer.sliceUpdatedSignal.connect(sliceSegToRaw)

        def mpRawToSeg(): segView.renderer.showMaximumProjection = rawView.renderer.showMaximumProjection
        def mpSegToRaw(): rawView.renderer.showMaximumProjection = segView.renderer.showMaximumProjection
        rawView.renderer.showMaximumProjectionSignal.connect(mpRawToSeg)
        segView.renderer.showMaximumProjectionSignal.connect(mpSegToRaw)

        def xlimRawToSeg():segView.renderer.xlim= rawView.renderer.xlim
        def xlimSegToRaw():rawView.renderer.xlim= segView.renderer.xlim
        def ylimRawToSeg():segView.renderer.ylim= rawView.renderer.ylim
        def ylimSegToRaw():rawView.renderer.ylim= segView.renderer.ylim
        rawView.renderer.xlimChangedSignal.connect(xlimRawToSeg)
        segView.renderer.xlimChangedSignal.connect(xlimSegToRaw)
        rawView.renderer.ylimChangedSignal.connect(ylimRawToSeg)
        segView.renderer.ylimChangedSignal.connect(ylimSegToRaw)

        def ppRawToSeg(): segView.renderer.projectionPlane= rawView.renderer.projectionPlane
        def ppSegToRaw(): rawView.renderer.projectionPlane = segView.renderer.projectionPlane
        rawView.renderer.projectionPlaneSignal.connect(ppRawToSeg)
        segView.renderer.projectionPlaneSignal.connect(ppSegToRaw)

        segMan = SegmentationManager(rawView, segView, elementsImageNode = editionImgNode)
        segSplitter = SegmentationSplitter(rawImg=rawView, segImg=segView, manager=segMan)

        self._mw.createDockableWidget(segSplitter,
                                      "Segmentation connector",
                                      dockAreaId=MW.DockAreaId.Right,
                                      hideOnClose=False)

    def selectPredictionImage(self):
        nodes = [n for n in self._smUI.selectedNodes if isinstance(n, Image) and n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")
        if len(nodes) == 1:
            self._mw.warningMsg('Please select at least raw and prediction image')
        elif len(nodes)==2:
            items = (nodes[0].name, nodes[1].name)
            item, ok = Qt.QInputDialog.getItem(self._mw, 'Segmentation editor', 'Select prediction image', items, 0, False)
            if ok and item:
                _indexPred = items.index(item)
                if _indexPred == 0:
                    _indexRaw = 1
                elif _indexPred == 1:
                    _indexRaw = 0
                rawView = Img3Viewer(nodes[_indexRaw])
                segView = Img3Viewer(nodes[_indexPred])
                elementsImageNode = Image(name='edition_' + nodes[_indexPred].name)
                SC.Scene().addNode2Parent(elementsImageNode, parent=nodes[_indexPred])
                self.addViewers(rawView, segView, elementsImageNode)
            else:
                self._mw.warningMsg("Nothing selected")
        elif len(nodes) == 3:
            dlg = CustomDialog(nodes, ('Raw', 'Prediction', 'Edition'))
            if dlg.exec_():
                print("Success!")
                rawView = Img3Viewer(dlg.imagesNode['Raw'])
                segView = Img3Viewer(dlg.imagesNode['Prediction'])
                self.addViewers(rawView, segView, dlg.imagesNode['Edition'])
            else:
                print("Cancel!")


def init(menuPath=None):
    SegmentationConnector(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys

    app = Qt.QApplication(sys.argv)

    imageNode = Image(name='Test')
    img = np.zeros((3, 6, 10), dtype='uint8')
    img[:, 0:3, 0:7] = np.ones((3, 3, 7))*3
    img[:, 0:4, 0:4] = np.ones((3, 4, 4))*3
    img[:, 0:6, 0:2] = np.ones((3, 6, 2))*3

    img[2:3, 3:4, 2:4] = np.ones((1, 1, 1))
    img[:, 4:6, 3:5] = np.ones((3, 2, 2))
    img[:, 4:6, 9:10] = np.ones((3, 2, 1))

    imageNode.img = img
    img[:, 4:6, 6:8] = np.ones((3, 2, 2))*3
    ex = Img3Viewer(imageNode)
    segMan = SegmentationManager(ex,  ex)
    segSplitter = SegmentationSplitter(rawImg=ex, segImg=ex, manager=segMan)

    segSplitter.show()
    sys.exit(app.exec())
