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
