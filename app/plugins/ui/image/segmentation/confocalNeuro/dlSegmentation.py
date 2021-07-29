# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:15:12 2019

@author: Isabel, Marcos García
"""
from app.core.ui import mainWindow as mw
from app.core.utils import SingletonDecorator
from app.core.model import scene as sc

from app.plugins.model.image.image import Image
from app.plugins.ui.sceneManagerUi import sceneManager as scm

from app.plugins.utils.image.segmentation import \
    UnetEvaluator, UnetModelManager


@SingletonDecorator
class DLSegmentationManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()
        self._sc = sc.Scene()

        self._menuPath = \
            ["Segmentation", "Deep Learning"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$DL##2"

        for name in UnetModelManager().getModelNames():
            self._mw.addAction(name, prefix=self._prefix)
            self._mw.addActionCB(
                name,
                lambda name=name: self._launchModel(name),
                prefix=self._prefix)
            self._mw.addAction2Menu(name,
                                    menuPath=self._menuPath,
                                    prefix=self._prefix)

    def _launchModel(self, modelName):
        nodes = [n for n in self._smUI.selectedNodes \
                 if isinstance(n, Image) and \
                 n.nDims == Image.Dims.img3D]

        if len(nodes) == 0:
            self._mw.warningMsg("No 3D images selected")
        else:
            if modelName is None or modelName == "":
                title = "Segmenting image set..."
            else:
                title = "Segmenting image set using " + modelName + "..."
            self._mw.processDialog(
                lambda: self._processNodeList(nodes, modelName), True,
                title=title,
                closeOnFinished=False)

    def _processNodeList(self, nodes, modelName):
        print("Loading model:", modelName)
        model = UnetEvaluator(modelName)

        print("\nThe following nodes will be segmented:")
        print(*(n.name for n in nodes), '\n')

        nNodes = len(nodes)
        progressInc = 100 // nNodes

        for i, n in enumerate(nodes):
            progressOffset = i * 100 // nNodes
            print("Segmenting {}.(Img {} out of {})".
                  format(n.name, 1 + i, nNodes))

            # todo:control de errores la imagen puede ser no valida
            #     opciones continuar con la siguiente imagen
            #     lanzar una excepción
            print("Preparing image")
            model.img = n.img
            model.infer()


            if model.prediction is None:
                raise ValueError("Segmenting error")

            node = Image(name="{} (Seg: {})".format(n.name, model.name))
            node.img = model.prediction
            self._sc.addNode2Parent(node, parent=n)
            print("    Node created:", node.name)

        yield 100



def init(menuPath=None):
    DLSegmentationManager(menuPath=menuPath)
