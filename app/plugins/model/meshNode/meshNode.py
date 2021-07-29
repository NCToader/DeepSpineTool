from app.core.model.sceneNode import SceneNode
import numpy as np


class MeshNode(SceneNode):
    def __init__(self, name=None, indices=None, vertices=None, normals = None):
        super().__init__(name)
        self.indices = indices
        self.vertices = vertices
        self.normals = normals

    def scale(self, factor):
        avgVertex = np.mean(self.vertices, axis=0)
        self.vertices = np.subtract(self.vertices, avgVertex)
        self.vertices = np.multiply(self.vertices, factor)
        self.vertices = np.add(self.vertices, avgVertex)

def init():
    meshnode = MeshNode()

