import vtk
import os
from PyQt5 import Qt

from app.core.model import scene as SC
from app.core.utils import SingletonDecorator
from vtk.util import numpy_support
from app.plugins.model.meshNode.meshNode import MeshNode
from app.core.ui.mainWindow import MainWindow
from app.plugins.ui.loaderManager import Loader


@SingletonDecorator
class MeshLoader(Loader):
    def __init__(self, *args):
        # UI
        self._menuPath = ["Mesh"]
        self._name = "Load mesh"
        super().__init__(*args)

    @classmethod
    def _cb(clss):
        filePath = MainWindow().loadFileDialog(filters=["STL (*.stl);; OBJ (*.obj);; All Files (*)"])
        if filePath is not None:
            filePath = filePath[0]
            node = list()

            extension = os.path.splitext(filePath)[1]
            if extension == '.stl':
                reader = vtk.vtkSTLReader()
            elif extension == '.obj':
                reader = vtk.vtkOBJReader()

            reader.SetFileName(filePath)
            reader.Update()
            mesh = reader.GetOutput()
            vtk_points = mesh.GetPoints()
            dataArray = vtk_points.GetData()
            indices_list = []
            numberOfFaces = mesh.GetNumberOfCells()
            faceIndex = vtk.vtkIdList()
            for i in range(0, numberOfFaces):
                mesh.GetCellPoints(i, faceIndex)
                vertexIndex0 = faceIndex.GetId(0)
                vertexIndex1 = faceIndex.GetId(1)
                vertexIndex2 = faceIndex.GetId(2)
                indices_list.append([vertexIndex0, vertexIndex1, vertexIndex2])
            data_np_array = numpy_support.vtk_to_numpy(dataArray)
            vertices_list = list(data_np_array)
            node = MeshNode(name=Qt.QFileInfo(filePath).fileName(), indices=indices_list, vertices=vertices_list)
            return node


    def sceneChange(self, **kwargs):
        print(kwargs)


if __name__ == '__main__':
    MeshLoader
