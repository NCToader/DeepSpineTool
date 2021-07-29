# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:27:29 2019

@author: URJC

#todo!!!!!!: OJO problemas de rendimiento. Se estan haciendo varios renderizados
             por solicitud de cambio de imagen.
#!todo: Botones pare el manejo en la ventana libre
#!todo: De forma general que no se cree un toolbar si no se va a utilizar!
#todo: https://scikit-image.org/docs/dev/api/skimage.filters.rank.html#skimage.filters.rank.modal
"""

import numpy as np
from PyQt5 import Qt

from app.plugins.model.image import Image
from app.plugins.utils.image import imgRange

from app.core.utils import SingletonDecorator
from app.core import ui as mw
from app.core.model import scene as sc
from app.core.ui.cbThread import CBLoopThread
from app.core.utils import SingletonDecorator
from app.plugins.model.image import Image
from app.plugins.ui import sceneManagerUi as scm
from app.plugins.ui.image.viewer.img3MultiProjViewer import Img3MultiProjViewer
from app.plugins.ui.image.viewer.img3MultiProjWidget import Img3MultiProjWidget

# from app.plugins.ui.qbasics.gridWidget import GridWidget
from app.plugins.ui.qbasics import CollapsableWidget

from app.plugins.ui.image.editor import modifiers


class Img3MultiProjEditor(Img3MultiProjViewer):

    @staticmethod
    def uiInit(parent, ui):
        # Main Widgets
        #############################################
        super().uiInit(parent, ui)
        parent.setObjectName("img3MultiProjEditor_form")

        panel_widget = parent.windowPanel
        panel_layout = panel_widget.layout()
        panel_layout.setDirection(Qt.QBoxLayout.TopToBottom)
        ui.editor_collapsable = CollapsableWidget(
            parent=panel_widget,
            position=CollapsableWidget.Position.Top)
        ui.viewer_collapsable = CollapsableWidget(
            parent=panel_widget,
            position=CollapsableWidget.Position.Top)
        ui.modifiers_widget = Qt.QWidget()
        ui.modifiers_widget.setSizePolicy(
            Qt.QSizePolicy.Preferred,
            Qt.QSizePolicy.Preferred)

        panel_layout.addWidget(ui.editor_collapsable)
        panel_layout.addWidget(ui.viewer_collapsable)
        panel_layout.addWidget(ui.modifiers_widget)

        # =============================================================================
        # Editor toolbar
        # =============================================================================
        ui.editor_widget = Qt.QWidget()
        ui.editor_widget.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)
        ui.editor_collapsable.addWidget(ui.editor_widget)
        ui.editor_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                         parent=ui.editor_widget)

        ui.createNew_pushButton = Qt.QPushButton(
            "Create new node",
            parent=ui.editor_widget)
        ui.createNew_pushButton.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)

        ui.apply_pushButton = Qt.QPushButton(
            "Apply to current node",
            parent=ui.editor_widget)
        ui.apply_pushButton.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)

        ui.reset_pushButton = Qt.QPushButton(
            "Reset",
            parent=ui.editor_widget)
        ui.reset_pushButton.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)

        ui.editor_layout.addWidget(ui.apply_pushButton)
        ui.editor_layout.addWidget(ui.createNew_pushButton)
        ui.editor_layout.addWidget(ui.reset_pushButton)

        # =============================================================================
        # Viewer toolbar
        # =============================================================================
        ui.viewer_widget = Qt.QWidget()
        ui.viewer_widget.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)
        ui.viewer_collapsable.addWidget(ui.viewer_widget)
        ui.viewer_layout = Qt.QBoxLayout(Qt.QBoxLayout.LeftToRight,
                                         parent=ui.viewer_widget)

        super(type(parent), parent).createMaximumProjectionCheckBox(
            ui.viewer_widget)
        ui.maximumProj_checkbox.setSizePolicy(
            Qt.QSizePolicy.Fixed,
            Qt.QSizePolicy.Fixed)

        ui.normalizedView_checkBox = Qt.QCheckBox(
            "Show image normalized",
            parent=ui.viewer_widget)
        ui.normalizedView_checkBox.setSizePolicy(Qt.QSizePolicy.Fixed,
                                                 Qt.QSizePolicy.Fixed)

        ui.viewer_layout.addWidget(ui.normalizedView_checkBox)

        # =============================================================================
        # Modifiers
        # =============================================================================
        ui.modifiers_layout = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom,
                                            parent=ui.modifiers_widget)

        ui.modifiers_tabWidget = Qt.QTabWidget(parent=ui.modifiers_widget)
        ui.modifiers_tabWidget.setSizePolicy(
            Qt.QSizePolicy.Expanding,
            Qt.QSizePolicy.Fixed)

        ui.modifiers_layout.addWidget(ui.modifiers_tabWidget)
        ui.modifiers_layout.addWidget(
            Qt.QWidget(parent=ui.modifiers_widget))

    def __init__(self, imageNode=None, parent=None, *args, **kwargs):
        self._mutex = Qt.QMutex()
        self._cbLoopThread = CBLoopThread()
        self._cbLoopThread.start()

        super().__init__(*args, imageNode, parent, **kwargs)

        self.modifiers = list()
        self._setInitialImg()

        self.addModifier("Contrast/brightness",
                         modifiers.ContrastBrightnessModifier(viewer=self))
        self.addModifier("Scaling",
                         modifiers.ScalingModifier(viewer=self))
        self.addModifier("Gamma Correction",
                         modifiers.GammaCorrectionModifier(viewer=self))
        self.addModifier("Log Correction",
                         modifiers.LogCorrectionModifier(viewer=self))
        self.addModifier("Sigmoid Correction",
                         modifiers.SigmoidCorrectionModifier(viewer=self))
        self.addModifier("Equalization",
                         modifiers.EqualizationModifier(viewer=self))
        self.addModifier("Adaptative Equalization",
                         modifiers.AdaptativeEqualizationModifier(viewer=self))
        self.addModifier("Contrast Streching",
                         modifiers.ContrastStrechingModifier(viewer=self))

        self._currentModifier = self._ui.modifiers_tabWidget.currentIndex()

        self._ui.createNew_pushButton.clicked.connect(self._createNew)
        self._ui.apply_pushButton.clicked.connect(self._apply)
        self._ui.reset_pushButton.clicked.connect(self._reset)
        self._ui.normalizedView_checkBox.stateChanged.connect(
            self._setPlotParams)

        self._ui.modifiers_tabWidget.currentChanged.connect(
            self._modifierChanged)

    def __del__(self):
        self._cbLoopThread.terminate()
        self._cbLoopThread.deletelater()

    @Qt.pyqtSlot()
    def _reset(self):
        self._cbLoopThread.waitForCB()

        if self.imageNode is None: return
        self.img = self._initialImg
        self._setInitialImg()

    @Qt.pyqtSlot()
    def _apply(self):
        self._cbLoopThread.waitForCB()

        if self.imageNode is None: return
        self.imageNode.img = self.img
        self._setInitialImg()

    @Qt.pyqtSlot()
    def _createNew(self):
        self._cbLoopThread.waitForCB()

        if self.imageNode is None: return

        node = Image(name="{} (Modified)".format(self.imageNode.name))
        node.img = self.img
        sc.Scene().addNode2Parent(node, parent=self.imageNode)
        self.imageNode = node

    @Qt.pyqtSlot()
    def _setPlotParams(self):
        self._cbLoopThread.waitForCB()
        resetParams = False
        if self._initialImg is not None:
            realmn, realmx = self.realRange

            if np.isscalar(realmn) and \
                    self._ui.normalizedView_checkBox.checkState() == Qt.Qt.Unchecked:
                self._ui.projViewers['xy'].renderer.setPlotParams(
                    vmin=realmn, vmax=realmx)
                self._ui.projViewers['zy'].renderer.setPlotParams(
                    vmin=realmn, vmax=realmx)
                self._ui.projViewers['xz'].renderer.setPlotParams(
                    vmin=realmn, vmax=realmx)
            else:
                resetParams = True

        else:
            resetParams = True

        if resetParams:
            self._ui.projViewers['xy'].renderer.setPlotParams()
            self._ui.projViewers['zy'].renderer.setPlotParams()
            self._ui.projViewers['xz'].renderer.setPlotParams()

    def _imgChangedCB(self, **kwargs):
        self._cbLoopThread.waitForCB()

        super()._imgChangedCB(**kwargs)
        self._setInitialImg()

    def _setInitialImg(self):
        self._cbLoopThread.waitForCB()

        self._initialImg = None if self.img is None else np.copy(self.img)

        if self._initialImg is not None:
            realmn, realmx, imgmn, imgmx = imgRange(self._initialImg)
            self._realRange = (realmn, realmx)
            self._imgRange = (imgmn, imgmx)

        else:
            self._realRange = None
            self._imgRange = None

        self._setPlotParams()

        if len(self.modifiers) > 0:
            self.modifiers[self._currentModifier].update()

    #        for m in self.modifiers:
    #            m.update()

    def _modifierChanged(self):
        self._cbLoopThread.waitForCB()

        changed = self.modifiers[self._currentModifier].changed

        if changed and not mw.MainWindow().confirmMsg(
                "Are you sure you want to continue?",
                info="If you continue, unsaved changes will be lost"):
            self._ui.modifiers_tabWidget.blockSignals(True)
            self._ui.modifiers_tabWidget.setCurrentIndex(self._currentModifier)
            self._ui.modifiers_tabWidget.blockSignals(False)
            return

        self._reset()

        self._currentModifier = self._ui.modifiers_tabWidget.currentIndex()
        self.modifiers[self._currentModifier].update()

    @property
    def realRange(self):
        return self._realRange

    @property
    def imgRange(self):
        return self._imgRange

    @Img3MultiProjViewer.imageNode.setter
    def imageNode(self, value):

        self._cbLoopThread.waitForCB()

        Img3MultiProjViewer.imageNode.fset(self, value)

        self._setInitialImg()

    @Img3MultiProjWidget.img.setter
    def img(self, value):
        #        super(Img3MultiProjWidget,self).img = value
        self._mutex.lock()
        Img3MultiProjWidget.img.fset(self, value)
        self._mutex.unlock()

    @property
    def initialImg(self):
        return self._initialImg

    @property
    def cbLoopThread(self):
        return self._cbLoopThread

    def addModifier(self, name, widget):

        self.modifiers.append(widget)
        self._ui.modifiers_tabWidget.addTab(widget, name)

    def createMaximumProjectionCheckBox(self, parent, *args, **kwargs):
        raise Warning("Function not implemented in " + type(self))


@SingletonDecorator
class Img3MultiProjEditorManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Image", "Editors"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "###~89234$$$"
        self._name = "Image 3D Multiprojection Editor"

        self._mw.addAction(self._name, prefix=self._prefix)
        self._mw.addActionCB(self._name,
                             self.addViewer,
                             prefix=self._prefix)
        self._mw.addAction2Menu(self._name,
                                menuPath=self._menuPath,
                                prefix=self._prefix)

    def addViewer(self):
        nodes = [n for n in self._smUI.selectedNodes \
                 if isinstance(n, Image) and \
                 n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")

        for imageNode in nodes:
            i3mpe = Img3MultiProjEditor(imageNode=imageNode)

            # !todo: No se pone el titulo porque habría que habilitar mecanismos
            #       para cerrar el widget y cambiar el titulo, si el nodo lo hace
            #            title = "Image 3D Viewer: " + imageNode.name
            self._mw.createDockableWidget(i3mpe,
                                          "Image 3D Multiprojection Editor",
                                          dockAreaId=mw.DockAreaId.Right,
                                          hideOnClose=False)


def init(menuPath=None):
    Img3MultiProjEditorManager(menuPath=menuPath)


if __name__ == '__main__':
    #    try:
    import sys

    app = Qt.QApplication(sys.argv)

    image = Image(name='Test')
    img = np.zeros((3, 6, 10, 3), dtype='int')
    img[:, 2:5, 4:7, :] = np.arange(3 * 3 * 3 * 3).reshape(3, 3, 3, 3)
    image.img = img

    ex = Img3MultiProjEditor()
    ex.imageNode = image

    ex.show()

    #        image.img[:, 2:5, 4:7, :] = 255*np.ones((3,3,3,3))
    #        type(image).img.touch(image)
    #
    image.img = (np.random.rand(40, 512, 512) * 50 + 100).astype(np.ubyte)

    sys.exit(app.exec())
