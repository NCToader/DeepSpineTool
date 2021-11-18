import vtk
from PyQt5 import Qt
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkCommonColor import vtkNamedColors

from app.core.model import scene as SC
from app.plugins.model.meshNode.meshNode import MeshNode
from app.plugins.model.image.image import Image

from app.core.ui import mainWindow as MW
from app.core.utils import SingletonDecorator
from app.plugins.ui.vtkViewer.ui_vtkManagerList import Ui_Form_VTKManager
from app.plugins.ui.vtkViewer.ui_vtkViewer import Ui_VTKViewer
import numpy as np

class VtkViewerList(Qt.QWidget):
    def __init__(self, parent=None, viewer=None):
        Qt.QMainWindow.__init__(self, parent)
        self.ui = Ui_Form_VTKManager()
        self.ui.setupUi(self)
        self._availableNodes = dict()
        self._activeNodes = dict()

        self.ui.pushButton_ImportNode.clicked.connect(self.add_node)
        self.ui.pushButton_RemoveNode.clicked.connect(self.remove_node)

        self.ui.availableNList.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        self.ui.activeNList.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)

        self.viewer = viewer
        sc = SC.Scene()
        sc.connect2Scene(self.scene_change)
        for node in sc.allSceneNode:
            if isinstance(node, MeshNode) or isinstance(node, Image):
                self.ui.availableNList.addItem(node.name)
                self._availableNodes[node.name] = node



    def remove_node(self):
        list1 = self.ui.activeNList
        list2 = self.ui.availableNList
        selectedItems = list1.selectedItems()
        for current_item in selectedItems:
            if current_item is not None:
                node_name = current_item.text()
                list2.addItem(node_name)
                list1.takeItem(list1.row(current_item))
                current_node = self._activeNodes.get(node_name)
                self._availableNodes[node_name] = current_node
                del self._activeNodes[node_name]
                self.viewer.removeNodeActor(node_name)

    def add_node(self):
        list1 = self.ui.availableNList
        list2 = self.ui.activeNList
        selectedItems = list1.selectedItems()
        for current_item in selectedItems:
            if current_item is not None:
                node_name = current_item.text()
                list2.addItem(node_name)
                list1.takeItem(list1.row(current_item))
                current_node = self._availableNodes.get(node_name)
                self._activeNodes[node_name] = current_node
                del self._availableNodes[node_name]
                if isinstance(current_node, MeshNode):
                    self.viewer.meshNode2actor(current_node)
                elif isinstance(current_node, Image):
                    self.viewer.imageNode2actor(current_node)

    def scene_change(self, op=None,
                     node=None,
                     oldParent=None,
                     newParent=None, **kwargs):
        if (op == 'nodeCreated'):
            if isinstance(node, MeshNode):
                self.ui.availableNList.addItem(node.name)
                self._availableNodes[node.name] = node

    @property
    def activeNodes(self):
        return self._activeNodes


class VtkViewer(Qt.QMainWindow, Ui_VTKViewer):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        self.ui = Ui_VTKViewer()
        self.ui.setupUi(self)
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.frame)
        self.ren = vtk.vtkRenderer()
        self.render()
        self._activeActors = dict()

    def render(self):
        self.ren.SetBackground(1, 1, 1)
        self.vtk_widget.GetRenderWindow().AddRenderer(self.ren)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        axes = vtkAxesActor()
        colors = vtkNamedColors()
        widget = vtkOrientationMarkerWidget()
        rgba = [0] * 4
        colors.GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(self.interactor)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        widget.SetEnabled(1)
        widget.InteractiveOn()

        self.ren.ResetCamera()

        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()
        self.interactor.Start()

    def meshNode2actor(self, node):
        # plane = vtk.vtkPlane()
        # plane.SetOrigin(0, 70, 0)
        # plane.SetNormal(0, 1, 0)
        # plane2 = vtk.vtkPlane()
        # plane2.SetOrigin(0, 0, 4)
        # plane2.SetNormal(0, 0, 1)

        points = vtk.vtkPoints()
        triangles = vtk.vtkCellArray()
        for i, tri in enumerate(node.indices):
            p1 = node.vertices[tri[0]]
            p2 = node.vertices[tri[1]]
            p3 = node.vertices[tri[2]]
            points.InsertNextPoint(*p1)
            points.InsertNextPoint(*p2)
            points.InsertNextPoint(*p3)

            triangle = vtk.vtkTriangle()

            triangle.GetPointIds().SetId(0, 3 * i + 0)
            triangle.GetPointIds().SetId(1, 3 * i + 1)
            triangle.GetPointIds().SetId(2, 3 * i + 2)
            triangles.InsertNextCell(triangle)
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetPolys(triangles)
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(poly_data)
        # mapper.AddClippingPlane(plane)
        # mapper.AddClippingPlane(plane2)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0, 0.5, 0.5)

        self.ren.AddActor(actor)
        self._activeActors[node.name] = actor
        self.render()

    def numpy_to_vtk(self, np_array):
        np_array = np.fliplr(np_array)
        dataImporter = vtk.vtkImageImport()
        img_data = np_array.astype('uint8')
        img_string = img_data.tostring()
        dim = np_array.shape
        dataImporter.CopyImportVoidPointer(img_string, len(img_string))
        dataImporter.SetDataScalarTypeToUnsignedChar()
        extent = dataImporter.GetDataExtent()
        dataImporter.SetDataExtent(extent[0], extent[0] + dim[1] - 1,
                                   extent[2], extent[2] + dim[2] - 1,
                                   extent[4], extent[4] + dim[0] - 1)
        dataImporter.SetWholeExtent(extent[0], extent[0] + dim[1] - 1,
                                    extent[2], extent[2] + dim[2] - 1,
                                    extent[4], extent[4] + dim[0] - 1)
        dataImporter.SetDataSpacing(0.0751562, 0.0751562, 0.279911)

        return dataImporter
    def addTiffToRender(self, vtkData):
        color_func = vtk.vtkColorTransferFunction()

        # 2. Filter --&gt; Setting the color mapper, Opacity for VolumeProperty
        color_func.AddRGBPoint(1, 1, 0.0, 0.0)  # Red

        # To set different colored pores
        color_func.AddRGBPoint(2, 0.0, 1, 0.0)  # Green

        opacity = vtk.vtkPiecewiseFunction()

        volume_property = vtk.vtkVolumeProperty()
        # set the color for volumes
        volume_property.SetColor(color_func)
        # To add black as background of Volume
        volume_property.SetScalarOpacity(opacity)
        volume_property.SetInterpolationTypeToNearest()
        volume_property.SetIndependentComponents(2)

        # Ray cast function know how to render the data
        volume_mapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()

        volume_mapper.SetInputConnection(vtkData.GetOutputPort())
        volume_mapper.SetBlendModeToMaximumIntensity()

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        return volume

    def addTiffClippingPlane(self, data):
        plane = vtk.vtkPlane()
        plane.SetOrigin(0, 70, 0)
        plane.SetNormal(0, 1, 0)
        plane2 = vtk.vtkPlane()
        plane2.SetOrigin(0, 0, 4)
        plane2.SetNormal(0, 0, 1)

        volume_mapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(data.GetOutputPort())
        volume_mapper.AddClippingPlane(plane)
        volume_mapper.AddClippingPlane(plane2)
        volume_mapper.SetBlendModeToComposite()

        color_func = vtk.vtkColorTransferFunction()

        # 2. Filter --&gt; Setting the color mapper, Opacity for VolumeProperty
        color_func.AddRGBPoint(1, 0, 1.0, 0.5)  # Green

        # To set different colored pores
        color_func.AddRGBPoint(2, 0.0, 0.5, 1.0)  # Blue

        opacity = vtk.vtkPiecewiseFunction()
        opacity.AddPoint(0,0)
        opacity.AddPoint(1, 1)
        opacity.AddPoint(2, 1)
        volume_property = vtk.vtkVolumeProperty()
        # set the color for volumes
        volume_property.SetColor(color_func)
        # To add black as background of Volume
        volume_property.SetScalarOpacity(opacity)
        volume_property.SetInterpolationTypeToNearest()
        volume_property.SetIndependentComponents(2)

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        return volume

    def imageNode2actor(self, node):
        volume = self.addTiffToRender(self.numpy_to_vtk(node.img))
        #volume = self.addTiffClippingPlane(self.numpy_to_vtk(node.img))
        self.ren.AddVolume(volume)
        self._activeActors[node.name] = volume
        self.render()

    def removeNodeActor(self, node_name):
        actor = self._activeActors.get(node_name)
        self.ren.RemoveActor(actor)
        self.render()


@SingletonDecorator
class VtkViewerManager():
    def __init__(self):
        self.mw = MW.MainWindow()
        self.mw.addAction("3D Viewer")
        self.mw.addAction2Menu("3D Viewer", ["Mesh", "Viewers"])
        self.mw.addActionCB("3D Viewer", self.openVTKViewer)

        self.countViewers = 0

    def openVTKViewer(self):
        self.countViewers += 1
        viewer = VtkViewer()
        self.mw.createDockableWidget(viewer.vtk_widget, "3D Viewer " + str(self.countViewers),
                                     dockAreaId=MW.DockAreaId.Right)
        viewerList = VtkViewerList(viewer=viewer)
        self.mw.createDockableWidget(viewerList, "3D Viewer " + str(self.countViewers) + " Manager",
                                     dockAreaId=MW.DockAreaId.Left)


def init():
    VtkViewerManager()
