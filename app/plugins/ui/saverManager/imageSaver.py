import traceback

from tifffile import imsave, imread

from app.core.ui import mainWindow as MW
from app.plugins.ui.sceneManagerUi import sceneManager as scm
from app.plugins.model.image.image import Image
from app.plugins.ui.saverManager import Saver


class BasicTiffSaver(Saver):
    def __init__(self, *args):
        self._menuPath = ["Image"]
        self._name = 'Save tiff'
        super().__init__(*args)

    @classmethod
    def _cb(clss):
        mw = MW.MainWindow()
        smUI = scm.SceneManagerUI()
        nodes = [n for n in smUI.selectedNodes if isinstance(n, Image) and n.nDims == Image.Dims.img3D]
        if len(nodes) == 0:
            mw.warningMsg("No 3D images selected")
        if len(nodes) > 1:
            mw.warningMsg('Please, select just one image')
        elif len(nodes)==1:
            array = nodes[0].img
            fn = mw.saveFileDialog(filters=['Tiff (*.tif)', 'All files(*)'])
            if fn is not None:
                imsave(fn[0], array)