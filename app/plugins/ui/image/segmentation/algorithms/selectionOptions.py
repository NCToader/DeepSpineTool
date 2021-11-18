from PyQt5 import Qt, QtWidgets, QtCore
from app.core.ui import mainWindow as MW
from app.plugins.utils.image.image import getAABBImg, idxAABB
import numpy as np
from skimage.segmentation import flood, flood_fill

class SelectionOptions(Qt.QWidget):
    class _UI:
        def __init__(self, parent, *args, **kwargs):
            parent.setObjectName("contrastBrightnessEditor_form")
            parent.setSizePolicy(Qt.QSizePolicy.Preferred,
                                 Qt.QSizePolicy.Preferred)

            self.so_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, parent=parent)

            thicknessLabelXY = Qt.QLabel('Selection thickness XY')
            self.thicknessSliderXY = Qt.QSlider(QtCore.Qt.Horizontal)
            self.thicknessSliderXY.setMinimum(1)
            self.thicknessSliderXY.setMaximum(10)
            self.thicknessSliderXY.setTickInterval(1)
            self.thicknessSliderXY.setTickPosition(Qt.QSlider.TicksBelow)
            thicknessHLayoutXY = QtWidgets.QHBoxLayout()
            thicknessHLayoutXY.addWidget(thicknessLabelXY)
            thicknessHLayoutXY.addWidget(self.thicknessSliderXY)

            thicknessLabelZ = Qt.QLabel('Selection thickness Z')
            self.thicknessSliderZ = Qt.QSlider(QtCore.Qt.Horizontal)
            self.thicknessSliderZ.setMinimum(1)
            self.thicknessSliderZ.setMaximum(10)
            self.thicknessSliderZ.setTickInterval(1)
            self.thicknessSliderZ.setTickPosition(Qt.QSlider.TicksBelow)
            thicknessHLayoutZ = QtWidgets.QHBoxLayout()
            thicknessHLayoutZ.addWidget(thicknessLabelZ)
            thicknessHLayoutZ.addWidget(self.thicknessSliderZ)

            self.keepElementBoundariesCB = Qt.QCheckBox('Keep element boundaries')
            self.keepElementBoundariesCB.setChecked(True)
            self.floodButton = Qt.QPushButton('Flood selection')
            hlayout = QtWidgets.QHBoxLayout()
            hlayout.addWidget(self.keepElementBoundariesCB)
            hlayout.addWidget(self.floodButton)

            self.so_layout.addLayout(thicknessHLayoutXY)
            self.so_layout.addLayout(thicknessHLayoutZ)
            self.so_layout.addLayout(hlayout)

    def __init__(self, viewer, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self._mw = MW.MainWindow()
        self._ui = SelectionOptions._UI(parent=self)
        self._viewer = viewer
        self._ui.thicknessSliderXY.valueChanged.connect(lambda: self.valueXYChanged(self._ui.thicknessSliderXY.value()))
        self._ui.thicknessSliderZ.valueChanged.connect(lambda: self.valueZChanged(self._ui.thicknessSliderZ.value()))
        self._ui.keepElementBoundariesCB.stateChanged.connect(lambda: self.cbState(self._ui.keepElementBoundariesCB))
        self._ui.floodButton.clicked.connect(self.floodSelection)

    def valueXYChanged(self, value):
        self._viewer.thicknessValueXY = value

    def valueZChanged(self, value):
        self._viewer.thicknessValueZ = value

    def cbState(self, cb):
        if cb.isChecked():
            self._viewer.keepElementBoundaries = True
        else:
            self._viewer.keepElementBoundaries = False

    def floodSelection(self):
        if self._viewer.viewer.renderer.showMaximumProjection:
            self._mw.warningMsg('Please deselect maximum projection')
        else:
            _z = self._viewer.viewer.renderer.sliceIdx
            selection = (self._viewer.viewer.img==3)
            mn, mx = getAABBImg(selection)
            aux_slices = idxAABB(mn, mx)
            slices = (slice(_z, _z+1), aux_slices[1], aux_slices[2])
            img = self._viewer.viewer.img[slices]
            com = np.zeros(2)
            sum = np.zeros(2)
            for _y in range(0, img.shape[1]):
                for _x in range(0, img.shape[2]):
                    com += img[0][_y][_x]*np.array([_y, _x])
                    sum += img[0][_y][_x]
            com/=sum
            com= (0, int(round(com[0])), int(round(com[1]))) #todo: com no siempre tiene sentido
            mask = flood_fill(img, com, 3, connectivity=1)
            auxImg = np.copy(self._viewer.viewer.img)
            auxImg[slices] = mask
            self._viewer.viewer.img = auxImg
            self._viewer.selection[np.where(self._viewer.viewer.img==3)] = True

