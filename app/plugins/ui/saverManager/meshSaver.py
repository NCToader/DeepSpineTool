from app.core.ui.mainWindow import MainWindow
from app.plugins.ui.saverManager import Saver
from app.core.ui import mainWindow as MW
from app.plugins.ui.sceneManagerUi import sceneManager as scm
from app.plugins.model.meshNode.meshNode import MeshNode
import os

def saveMesh( mesh, fn):
    faces = mesh.indices + 1
    verts = mesh.vertices
    normals = mesh.normals
    thefile = open(os.path.join(fn), 'w')
    for item in verts:
        thefile.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))
    if normals is not None:
        for item in normals:
            thefile.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))
    for item in faces:
        thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))
    thefile.close()

class MeshSaver(Saver):
    def __init__(self, *args):
        self._menuPath = ["Mesh"]
        self._name = 'Save mesh'
        super().__init__(*args)

    @classmethod
    def _cb(clss):
        mw = MW.MainWindow()
        smUI = scm.SceneManagerUI()
        nodes = [n for n in smUI.selectedNodes if isinstance(n, MeshNode)]
        if len(nodes) == 0:
            mw.warningMsg("No meshes selected")
        if len(nodes) > 1:
            pn = mw.saveDirectoryDialog()
            for node in nodes:
                fileName = pn + '/' + node.name + '.obj'
                saveMesh(node, fileName)
        elif len(nodes) == 1:
            fn = mw.saveFileDialog(filters=['OBJ (*.obj)', 'VRML (*.vrml)', 'All files(*)'])
            if fn is not None:
                saveMesh(nodes[0], fn[0])

