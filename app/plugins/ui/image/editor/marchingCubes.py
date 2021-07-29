from app.plugins.model.image import Image

from app.core import ui as mw
from app.core.model import scene as SC
from app.plugins.ui import sceneManagerUi as scm

from skimage import measure
from app.plugins.model.meshNode.meshNode import MeshNode


def marchingCubes(image):
    verts, faces, normals, values = measure.marching_cubes_lewiner(image.img, level=0.5)
    node = MeshNode(name=image.name, indices=faces, vertices=verts)
    SC.Scene().addNode2Parent(node, parent=image)


class marchingCubesManager:
    def __init__(self, menuPath=None):
        self._mw = mw.MainWindow()
        self._smUI = scm.SceneManagerUI()

        self._menuPath = ["Image", "Editors"] if menuPath is None else menuPath
        self._menuRoot = self._mw.createMenu(menuPath=self._menuPath)
        self._prefix = "%$%$2"
        self._name = "Marching cubes"

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
            marchingCubes(imageNode)


def init(menuPath=None):
    marchingCubesManager(menuPath=menuPath)
