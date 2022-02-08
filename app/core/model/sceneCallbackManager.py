# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:25:38 2019

@author: Marcos
#!todo: se podria hacer con un solo diccionario con partes de la clave a None
#!todo: comprobacion de tipos de las claves
"""

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

from app.core.utils import SingletonDecorator, CBSetManager, CBDictManager


@SingletonDecorator
class SceneCallbackManager():
    def __init__(self):
        self._sceneCB = CBSetManager()

        self._objAttribCB = CBDictManager()
        self._classAttribCB = CBDictManager()
        self._attribCB = CBDictManager()
        self._objCB = CBDictManager()
        self._classCB = CBDictManager()

    def updatedScene(self, **kwargs):
        self._sceneCB.call(**kwargs)

    def updatedAttrib(self, obj=None, attrib=None, **kwargs):
        if attrib is None or obj is None: return

        classList = obj.getClassNameHierarchy()
        # !todo: Esta es la única dependencia con la clase escena

        self._objAttribCB.call((obj, attrib), obj=obj, attrib=attrib, **kwargs)
        self._attribCB.call(attrib, obj=obj, attrib=attrib, **kwargs)
        self._objCB.call(obj, obj=obj, attrib=attrib, **kwargs)

        for className in classList:
            self._classCB.call(className,
                               obj=obj, attrib=attrib, **kwargs)
            self._classAttribCB.call((className, attrib),
                                     obj=obj, attrib=attrib, **kwargs)

    def removeObjAttribConnections(self, attrib=None, obj=None):
        if attrib is None or obj is None: return

        self._objAttribCB.removeKey((obj, attrib))

    def removeObjConnections(self, attrib=None, obj=None):
        if attrib is None or obj is None: return

        self._objACB.removeKey(obj)

    def connect2Scene(self, cb):
        self._sceneCB.registerCB(cb)

    def connect2ObjAttrib(self, cb, obj=None, attrib=None):
        if attrib is None or obj is None: return
        # !todo: se podría levantar un error

        self._objAttribCB.registerCB((obj, attrib), cb)

    def connect2ClassAttrib(self, cb, class_=None, attrib=None):
        if attrib is None or class_ is None: return

        className = class_.__name__

        self._classAttribCB.registerCB((className, attrib), cb)

    def connect2Attrib(self, cb, attrib=None):
        if attrib is None: return
        self._attribCB.registerCB(attrib, cb)

    def connect2Obj(self, cb, obj=None):
        if obj is None: return
        self._objCB.registerCB(obj, cb)

    def connect2Class(self, cb, class_=None):
        if class_ is None: return

        className = class_.__name__

        self._classCB.registerCB(className, cb)

    def disconnectFromScene(self, cb):
        self._sceneCB.unregisterCB(cb)

    def disconnectFromObjAttrib(self, cb, attrib=None, obj=None):
        if attrib is None or obj is None: return
        # !todo: se podría levantar un error

        self._objAttribCB.unregisterCB((obj, attrib), cb)

    def disconnectFromClassAttrib(self, cb, attrib=None, class_=None):
        if attrib is None or class_ is None: return

        className = class_.__name__

        self._classAttribCB.unregisterCB((className, attrib), cb)

    def disconnectFromAttrib(self, cb, attrib=None):
        if attrib is None: return
        self._attribCB.unregisterCB(attrib, cb)

    def disconnectFromObj(self, cb, obj=None):
        if obj is None: return
        self._objCB.unregisterCB(obj, cb)

    def disconnectFromClass(self, cb, class_=None):
        if class_ is None: return

        className = class_.__name__

        self._classCB.unregisterCB(className, cb)
