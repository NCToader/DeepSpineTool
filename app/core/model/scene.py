# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:45:50 2019

@author: Marcos
#!todo:  1. Gestion de unidades
         2. Comprobación de la coherencia de un nodo.
            Busqueda de ciclos...
"""

from copy import copy

import pickle as pk
import bz2
# !todo: IMPORTANTE pickle no es seguro!!!!

from app.core.model.sceneCallbackManager import SceneCallbackManager
from app.core.model.sceneNode import SceneNode

from app.core.utils import SingletonDecorator


@SingletonDecorator
class Scene():
    def __init__(self):
        self._children = set()
        self._allNodes = set()
        self._SCM = SceneCallbackManager()

        self._name = "SCENE"

    #        self._units = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    # =============================================================================
    #   Propiedades
    # =============================================================================
    @property
    def name(self):
        return self._name

    # !Todo: los atributos de escena deben de tener su propio sistema de CBs

    @name.setter
    def name(self, value):
        self._name = value
        self._SCM.updatedScene(op="nameChanged", name=value)

    @property
    def parent(self):
        return None

    @property
    def children(self):
        return copy(self._children)

    @property
    def allSceneNode(self):
        return copy(self._allNodes)

    # =============================================================================
    #   Conexion de objetos
    # =============================================================================
    def connect2Scene(self, cb):
        self._SCM.connect2Scene(cb)

    def disconnectFromScene(self, cb):
        self._SCM.disconnectFromScene(cb)

    # =============================================================================
    #   Manipulación de la escena
    # =============================================================================
    def isAdded2Scene(self, node):
        return node in self._allNodes

    def addNode2Parent(self, node, parent=None, **kwargs):
        SceneNode.checkIsSubClass(node)

        if parent is None:
            parent = self
        elif not self.isAdded2Scene(parent):
            raise ValueError(
                "Error: parent node does not belong to the scene")
        else:
            SceneNode.checkIsSubClass(parent)

        if node.parent is not None:
            oldParent = node.parent
            if parent == oldParent: return
            op = "nodeMoved"
            node.parent._removeChild(node)
        else:
            op = "nodeCreated"
            oldParent = None

            self._allNodes.add(node)

        parent._addChild(node)
        node._addParent(parent, **kwargs)
        # se actualizan los hijos que lo necesiten

        self._SCM.updatedScene(op=op,
                               node=node,
                               oldParent=oldParent,
                               newParent=parent,
                               **kwargs)

    def removeSceneNode(self, node, **kwargs):
        SceneNode.checkIsSubClass(node)

        if not self.isAdded2Scene(node):
            raise ValueError(
                "Error: node does not belong to the scene")

        oldParent = node.parent

        for n in node.children:
            self.removeSceneNode(n, **kwargs)

        node._removeConnections()

        node.parent._removeChild(node)
        self._allNodes.remove(node)
        node._parent = None

        self._SCM.updatedScene(op="nodeRemoved",
                               node=node,
                               oldParent=oldParent,
                               **kwargs)

    # =============================================================================
    #   Protegidos
    # =============================================================================
    def _addChild(self, node):
        self._children.add(node)

    def _removeChild(self, node):
        self._children.remove(node)

    # =============================================================================
    #   Sereializadores
    # =============================================================================
    def new(self):
        for n in self.children:
            self.removeSceneNode(n)

        self.name = "SCENE"

    def savez(self, filename):
        try:
            f = bz2.BZ2File(filename, 'wb')
        except:
            return False

        for n in self._children:
            n._parent = None

        pk.dump(["MagicWord:CBB", self._name, self._children], f)

        for n in self._children:
            n._parent = self

        f.close()

        return True

    def loadz(self, filename):
        class RestrictedUnpickler(pk.Unpickler):
            pass

        #            def find_class(self, module, name):
        #                # Only allow safe classes from builtins.
        #                if module == "builtins" and name in safe_builtins:
        #                    return getattr(builtins, name)
        #                # Forbid everything else.
        #                raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
        #                                             (module, name))
        #                    print ("Module: %s. Name: %s " % (module, name))
        #                    super().find_class(module, name)

        loaded = True
        try:
            f = bz2.BZ2File(filename, 'rb')
            p = RestrictedUnpickler(f)
            obj = p.load()
            #        obj = pk.load(f)

            if obj[0] != "MagicWord:CBB": return False

            self.new()
            self.name = obj[1]

            for n in obj[2]:
                n._parent = None

            def addNode(node):
                children = node.children
                node._children = set()

                parent = node.parent
                node._parent = None

                self.addNode2Parent(node, parent)

                for n in children:
                    addNode(n)

            for n in obj[2]:
                addNode(n)

        except:
            loaded = False
        finally:
            f.close()
            return loaded

    # =============================================================================
    #   Acceso a Clase
    # =============================================================================
    @classmethod
    def getClass(class_):
        return class_

    @classmethod
    def getClassNameHierarchy(class_):
        return [class_.__name__]

    @classmethod
    def getClassHierarchy(class_):
        return [class_]

    @classmethod
    def getClassName(class_):
        return class_.__name__


####################################################################

#    def checkCoherent(self, node):
#        SceneNode.checkIsSubClass(node)
#
#        if np.logical_xor( node.getParent() is None,
#                           not (node in self._allNodes)):
#             raise ValueError("Error: Inconsistent Scene")
#
#        if node.getParent() is None:
#            if len(node.getChildren()) != 0:
#                raise ValueError("Error: Inconsistent Scene")
#        elif not node in node.getParent().getChildren():
#             raise ValueError("Error: Inconsistent Scene")
#
#        #falta comprobar la coherencia de los hijos
#
#        return  True

####################################################################

# equivalente más legible y  lento

####################################################################

if __name__ == '__main__':
    import numpy as np

    sceneTest = True
    hierarchyTest = False
    sceneCallbackTest = 0

    callbackTest = 0
    saveTest = True


    class C1(SceneNode):
        pass


    class C11(C1):
        pass


    class C2(SceneNode):
        pass


    def scCB(op=None, node=None, oldParent=None, newParent=None, **kwarg):

        print("#############################################################")
        print("scCB: ")
        print("#############################################################")

        def printData(data, name, val, koString, ):
            if data is not None:
                print(name, val)
            else:
                print(name, koString)

        printData(op, "OP: ", op, "NONE")
        printData(node, "Node: ", node.name, "NONE")
        printData(oldParent, "Old Parent: ", oldParent, "NONE")
        printData(newParent, "New Parent", newParent, "NONE")
        print("Dictionary: ", kwarg)


    def printNodeList(nodeList):
        for n in nodeList:
            print(" ")
            print("Nombre del nodo: ", n.name, n.getClassName())
            print("-- Padre: ", n.parent.name if n.parent is not None else None)
            print("-- Hijos: ", [n.name for n in n.children])


    c1 = C1("obj1")
    c11 = C11("obj11")
    c2 = C2("obj2")
    c2b = C2("obj2b")
    c = [c1, c11, c2, c2b]

    # =============================================================================
    #     Test de escena
    # =============================================================================
    if sceneTest:
        s1 = Scene()
        s2 = Scene()

        print('Singleton test: ' + str(s1 == s2))

        nodeList = [SceneNode(str(i)) for i in range(5)]

        n_old = nodeList[0]
        s2.addNode2Parent(n_old)
        for n in nodeList[1:len(nodeList)]:
            s2.addNode2Parent(n, parent=n_old)
            n_old = n

        printNodeList(nodeList)

        s2.addNode2Parent(nodeList[2])
        s2.addNode2Parent(nodeList[4], parent=nodeList[0])

        printNodeList(nodeList)

        nodeList[0].transform = np.eye(4) * 2
        print(nodeList[4].globalTransform)

        print("xxxxxxxxxxxxxxxx")
        s1.removeSceneNode(nodeList[0])

    # =============================================================================
    #     Test de escena
    # =============================================================================
    if hierarchyTest:

        printNodeList(c)

        print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("C11")
        print(c11.getClass())
        print(C11.getParentClassName())
        print(C11.getClassNameHierarchy())
        print(c11.getClassHierarchy())

        print("C2")
        print(C2.getClassNameHierarchy())

        print("xxxxxxxxxxxxxxxxxxxxxxxx")

        try:
            C11.checkIsSubClass(c11)
            C11.checkIsSubClass(c1)
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)

    # =============================================================================
    #     Test de CB
    # =============================================================================

    if sceneCallbackTest != 0:

        s = Scene()

        s.connect2Scene(scCB)
        if sceneCallbackTest != 1: s.disconnectFromScene(scCB)

        s.addNode2Parent(c1)
        s.addNode2Parent(c11, parent=c1)
        s.addNode2Parent(c2, parent=c1)
        s.addNode2Parent(c2b, parent=c2)

        printNodeList(c)

        s.addNode2Parent(c2, parent=c11)

        printNodeList(c)

        s.removeSceneNode(c2)

        printNodeList(c)

    if callbackTest != 0:

        s = Scene()

        c2b.connect2Obj(occCB)
        if callbackTest != 1: c2b.disconnectFromObj(occCB)
        c2b.connect2Class(occCB)
        if callbackTest != 2: c2b.disconnectFromClass(occCB)
        c2b.connect2ObjAttrib(occCB, SceneNode.name)
        if callbackTest != 3:
            c2b.disconnectFromObjAttrib(occCB, SceneNode.name)
        c2b.connect2ClassAttrib(occCB, SceneNode.name)
        if callbackTest != 4:
            c2b.disconnectFromClassAttrib(occCB, SceneNode.name)
        SceneNode.name.connect2Attrib(occCB)
        if callbackTest != 5: SceneNode.name.disconnectFromAttrib(occCB)
        #
        c2b.name = "c2bbbbb"
        c2.name = "CC2"

        c1.transform = np.eye(4) * 3

        print("Add c1 xxxxxxxxxx")
        s.addNode2Parent(c1)
        print("Add c11 to c1 xxxxxxxxxx")
        s.addNode2Parent(c11, parent=c1)
        print("Add c2 to c1 xxxxxxxxxx")
        s.addNode2Parent(c2, parent=c1)
        print("Add c2 to c2b xxxxxxxxxx")
        s.addNode2Parent(c2b, parent=c2)
        print("Move c2 to c11 xxxxxxxxxxxxxxxxxxxxxxxxx")
        s.addNode2Parent(c2, parent=c11)

        print("c1 transform")
        c1.transform = np.eye(4) * 2

        print("Remove c2 xxxxxxxxxxxxxxxxxxxxx")
        s.removeSceneNode(c2)

        print("c1 transform")
        c1.transform = np.eye(4) * 4

        print("c2b final name change")
        c2b.name = "c2bbbbb"

        printNodeList(c)

    # =============================================================================
    #     Save Test
    # =============================================================================
    if (saveTest):
        s = Scene()

        print("Add c1 xxxxxxxxxx")
        s.addNode2Parent(c1)
        print("Add c11 to c1 xxxxxxxxxx")
        s.addNode2Parent(c11, parent=c1)
        print("Add c2 to c1 xxxxxxxxxx")
        s.addNode2Parent(c2, parent=c1)
        print("Add c2 to c2b xxxxxxxxxx")
        s.addNode2Parent(c2b, parent=c2)

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        printNodeList(c)

        s.savez("test.scene")

        s.addNode2Parent(c2, parent=c11)

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        printNodeList(c)

        s.loadz("test.scene")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(list(s._children)[0]._children)
