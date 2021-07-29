# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:00:22 2019

@author: Marcos
"""

# External import
import numpy as np
import inspect as ins
from copy import copy

# Core import
from app.core.model.sceneProperty import ScnPropDecorator, SceneProperty
from app.core.model.sceneCallbackManager import SceneCallbackManager


class SceneNode():
    _SCM = SceneCallbackManager()

    # !Todo: Sustituir por un inicializador?

    def __init__(self, name=""):
        if self.getClass()._SCM is None:
            raise TypeError("SceneProperty is not initialized")

        self._name = name
        self._transform = np.eye(4)

        self._parent = None
        self._children = set()

        self._hashId = id(self)

    # =============================================================================
    #   Atributos
    # =============================================================================
    #    @ScnPropDecorator() # ID automático
    @ScnPropDecorator(attribID="SceneNode.name",
                      validType=str)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @ScnPropDecorator(attribID="SceneNode.transform",
                      validType=np.ndarray)
    def transform(self):
        return np.copy(self._transform)

    @transform.setter
    def transform(self, value):
        self._transform[0:4, 0:4] = value

    @transform.postupdater
    def transform(self):
        self.getClass().globalTransform.touch(self)

    @transform.valuevalidator
    def transform(self, value):
        return value.shape == (4, 4)

    @ScnPropDecorator(attribID="SceneNode.globalTransform")
    def globalTransform(self):
        def getGlobalTransform(node):
            if isinstance(node.parent, SceneNode):
                parentGT = getGlobalTransform(node.parent)
                return np.matmul(parentGT,
                                 node._transform)
            else:
                return node.transform

        return getGlobalTransform(self)

    @globalTransform.postupdater
    def globalTransform(self, **kwargs):
        for n in self.children:
            n.getClass().globalTransform.touch(n, **kwargs)

    # @SceneProperty
    @property
    def parent(self):
        return self._parent

    # @SceneProperty
    @property
    def children(self):
        return copy(self._children)

    # =============================================================================
    #  Setters friend y protegidas para los attributos de acceso restrigidos
    # =============================================================================

    def _addChild(self, node):
        self._children.add(node)

    #        for n in self.children:
    #            SceneNode.globalTransform.updated(n, **kwargs)

    def _removeChild(self, node):
        self._children.remove(node)

    #        for n in self.children:
    #            SceneNode.globalTransform.updated(n, **kwargs)

    def _addParent(self, node, **kwargs):
        self._parent = node
        self.getClass().globalTransform.touch(self, **kwargs)

    def _removeConnections(self):
        for var in ins.getmembers(self.__class__,
                                  lambda a: isinstance(a, SceneProperty)):
            var[1].removeConnections(self)

        self.getClass()._SCM.removeObjConnections(obj=self)

    # =============================================================================
    #   Clases internas para indexado
    # =============================================================================
    def __hash__(self):
        return hash(self._hashId)

    def __eq__(self, other):
        if isinstance(other, SceneNode):
            return self._hashId == other._hashId
        else:
            return False

    # =============================================================================
    #   Métodos estáticos y no estaticos de acceso a la clase
    # =============================================================================
    @classmethod
    def getClass(class_):
        return class_

    @classmethod
    def getClassNameHierarchy(class_):
        classList = [class_.__name__]
        nextClass = class_.__bases__[0]

        while issubclass(nextClass, SceneNode):
            classList.append(nextClass.__name__)
            nextClass = nextClass.__class__.__bases__[0]

        return classList

    @classmethod
    def getClassHierarchy(class_):
        classList = [class_]
        nextClass = class_.__bases__[0]

        while issubclass(nextClass, SceneNode):
            classList.append(nextClass)
            nextClass = nextClass.__class__.__bases__[0]

        return classList

    @classmethod
    def getClassName(class_):
        return class_.__name__

    #    @classmethod
    #    def getParentClassName(class_):
    #        return class_.__bases__[0].__name__

    @classmethod
    def checkIsSubClass(class_, node):
        if not issubclass(node.__class__, class_):
            # https://docs.python.org/3/library/exceptions.html - ValueError
            raise TypeError(
                "Error: {} is not a {} object".format(
                    node, class_.__name__))

        return True

    # =============================================================================
    #   Conexion de objetos
    # =============================================================================
    def connect2ObjAttrib(self, cb, attrib):
        self.getClass()._SCM.connect2ObjAttrib(
            cb,
            obj=self,
            attrib=attrib)

    def connect2Obj(self, cb):
        self.getClass()._SCM.connect2Obj(cb, obj=self)

    @classmethod
    def connect2ClassAttrib(class_, cb, attrib):
        class_._SCM.connect2ClassAttrib(
            cb,
            class_=class_,
            attrib=attrib)

    @classmethod
    def connect2Class(class_, cb):
        class_._SCM.connect2Class(cb, class_=class_)

    def disconnectFromObjAttrib(self, cb, attrib):
        self.getClass()._SCM.disconnectFromObjAttrib(
            cb,
            obj=self,
            attrib=attrib)

    def disconnectFromObj(self, cb):
        self.getClass()._SCM.disconnectFromObj(cb, obj=self)

    @classmethod
    def disconnectFromClassAttrib(class_, cb, attrib):
        class_._SCM.disconnectFromClassAttrib(
            cb,
            class_=class_,
            attrib=attrib)

    @classmethod
    def disconnectFromClass(class_, cb):
        class_._SCM.disconnectFromClass(cb, class_=class_)
