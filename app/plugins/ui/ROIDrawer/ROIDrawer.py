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

import numpy as np
from PyQt5 import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

from app.core.model import scene as SC
from app.core.model import sceneCallbackManager as SCM
from app.core.ui import mainWindow as MW
from app.core.utils import SingletonDecorator
from app.plugins.ui.ROIDrawer.ui_roiViewer import Ui_ROIviewer
from app.plugins.ui.sceneManagerUi import sceneManager as SM
import os
from skimage import io
from app.plugins.model.image.image import Image

class ROICanvas():
    def __init__(self, img=None, id=None):
        # img0 = np.max_(img3D, axis=0)
        self.id = id
        self.fig0 = Figure()
        self.ax = self.fig0.add_subplot(111)
        self.ax.imshow(img)

        self.canvas = FigureCanvas(self.fig0)
        self.canvas.draw()
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.init_coord = None
        self.end_coord = None
        self.rs = RectangleSelector(self.ax, self.onselect, drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels', interactive=True)

    def onselect(self, eclick, erelease):
        "eclick and erelease are matplotlib events at press and release."
        print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
        print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        self.init_coord = eclick
        self.end_coord = erelease
        scm = SCM.SceneCallbackManager()
        scm.updatedScene(op='rsSelected', id=self.id, extents=self.rs.extents)


class ROIViewer(Qt.QWidget):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        self.ui = Ui_ROIviewer()
        self.ui.setupUi(self)
        sm = SM.SceneManagerUI()
        if isinstance(sm.currentNode, Image):
            self.img = sm.currentNode.img
        else:
            self.img = np.arange(512 * 512 * 128).reshape((128, 512, 512))

        self.canvas_dict = dict()
        self.pltIMG(self.img)
        self.show()
        sc = SC.Scene()
        sc.connect2Scene(self.scene_change)

    def scene_change(self, op=None, id=None, extents=None, **kwargs):
        print(kwargs)
        if (op == 'rsSelected'):
            if id == 0:
                if (self.canvas_dict.get(1).rs.extents[0] == 0 and self.canvas_dict.get(1).rs.extents[1] == 0):
                    self.canvas_dict.get(1).rs.extents = (extents[0], extents[1], 0, self.img.shape[0])
                else:
                    self.canvas_dict.get(1).rs.extents = (extents[0], extents[1], self.canvas_dict.get(1).rs.extents[2],
                                                          self.canvas_dict.get(1).rs.extents[3])
                if (self.canvas_dict.get(2).rs.extents[0] == 0 and self.canvas_dict.get(2).rs.extents[1] == 0):
                    self.canvas_dict.get(2).rs.extents = (extents[2], extents[3], 0, self.img.shape[0])
                else:
                    self.canvas_dict.get(2).rs.extents = (extents[2], extents[3], self.canvas_dict.get(2).rs.extents[2],
                                                          self.canvas_dict.get(2).rs.extents[3])
            if id == 1:
                if (self.canvas_dict.get(0).rs.extents[0] == 0 and self.canvas_dict.get(0).rs.extents[1] == 0):
                    self.canvas_dict.get(0).rs.extents = (extents[0], extents[1], 0, self.img.shape[1])
                else:
                    self.canvas_dict.get(0).rs.extents = (extents[0], extents[1], self.canvas_dict.get(0).rs.extents[2],
                                                          self.canvas_dict.get(0).rs.extents[3])
                if (self.canvas_dict.get(2).rs.extents[0] == 0 and self.canvas_dict.get(2).rs.extents[1] == 0):
                    self.canvas_dict.get(2).rs.extents = (0, self.img.shape[1], extents[2], extents[3])
                else:
                    self.canvas_dict.get(2).rs.extents = (self.canvas_dict.get(2).rs.extents[0],
                                                          self.canvas_dict.get(2).rs.extents[1], extents[2], extents[3])
            if id == 2:
                if (self.canvas_dict.get(0).rs.extents[0] == 0 and self.canvas_dict.get(0).rs.extents[1] == 0):
                    self.canvas_dict.get(0).rs.extents = (0, self.img.shape[2], extents[0], extents[1])
                else:
                    self.canvas_dict.get(0).rs.extents = (self.canvas_dict.get(0).rs.extents[0],
                                                          self.canvas_dict.get(0).rs.extents[1], extents[0], extents[1])
                if (self.canvas_dict.get(1).rs.extents[0] == 0 and self.canvas_dict.get(1).rs.extents[1] == 0):
                    self.canvas_dict.get(1).rs.extents = (0, self.img.shape[2], extents[2], extents[3])
                else:
                    self.canvas_dict.get(1).rs.extents = (self.canvas_dict.get(1).rs.extents[0],
                                                          self.canvas_dict.get(1).rs.extents[1], extents[2], extents[3])

    def pltIMG(self, img3D):
        self.ui.ROIgl.setColumnStretch(0, 4)
        self.ui.ROIgl.setColumnStretch(1, 4)
        self.canvas_list = []

        for i in range(3):
            img = np.max(img3D, axis=i)
            canvas = ROICanvas(img=img, id=i)
            self.ui.ROIgl.addWidget(canvas.canvas)
            self.show()
            self.canvas_list.append(canvas)
            self.canvas_dict[i] = canvas

        createButton = Qt.QPushButton('Create ROI')
        self.ui.ROIgl.addWidget(createButton)
        createButton.clicked.connect(self.createROI)

    def save_tif(self, file, filename):
        if not os.path.isfile(filename + '.tif'):
            io.imsave(filename + '.tif', file)
        else:
            print('File already exists, not saving')

    def show_save_TIFF_dialog(self, img):
        options = Qt.QFileDialog.Options()
        options |= Qt.QFileDialog.DontUseNativeDialog
        fileName, _ = Qt.QFileDialog.getSaveFileName(self, "Save tiff", "", "Tiff (*.tif);; All Files (*)",
                                                     options=options)
        if fileName:
            self.save_tif(img, fileName)

    def createROI(self):
        print('Save ROI clicked')
        extents0 = self.canvas_dict.get(0).rs.extents
        extents1 = self.canvas_dict.get(1).rs.extents
        imgROI = self.img[int(round(extents1[2])):int(round(extents1[3])),
                 int(round(extents0[2])):int(round(extents0[3])), int(round(extents0[0])):int(round(extents0[1]))]
        # imgROI = self.img[coords[5]:coords[7], coords[0]:coords[2], coords[1]:coords[3]]
        print(imgROI.shape)
        node = Image(name='ROI')
        node.img = imgROI
        SC.Scene().addNode2Parent(node=node, parent=SM.SceneManagerUI().currentNode)
        # self.show_save_TIFF_dialog(imgROI)


@SingletonDecorator
class ROIDrawer():
    def __init__(self):
        # UI
        self.mw = MW.MainWindow()
        self.mw.addAction("&Create ROI")
        self.mw.addAction2Menu("&Create ROI", ["Tools"])
        self.mw.addActionCB("&Create ROI", self.open_drawer)

    def open_drawer(self):
        viewer = ROIViewer()
        self.mw.createDockableWidget(viewer, "ROI Viewer", dockAreaId=MW.DockAreaId.Right)


def init():
    roi = ROIDrawer()
