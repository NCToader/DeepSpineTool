# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:50:05 2019

@author: Marcos
https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work

#!todo: REVISA EL TEMA DE CALLBACKS Y HERENCIAS, puede que se llame al get del
#      padre si no se hace bien!!!!!
#!todo: Hacer que el validator no solo devuelva true o false sino la cadena de 
#       error
#!todo: Pasar el valor en el updated para no tener que acceder 
        a través del __get__. Importancia baja
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

from typing import Iterable
from inspect import isclass

from app.core.model.sceneCallbackManager import SceneCallbackManager


def ScnPropDecorator(attribID=None,
                     validType=None):
    #                     valueRange = None):
    if attribID is None:
        ID = "__@%" + str(ScnPropDecorator.FreeID) + "%@__"
        ScnPropDecorator.FreeID = ScnPropDecorator.FreeID + 1
        while attribID in ScnPropDecorator.attribIDList:
            ID = "__@%" + str(ScnPropDecorator.FreeID) + "%@__"
            ScnPropDecorator.FreeID = ScnPropDecorator.FreeID + 1
    else:
        ID = attribID

    if ID in ScnPropDecorator.attribIDList:
        raise ValueError("ID {} already exits".format(ID))
    else:
        ScnPropDecorator.attribIDList.append(ID)

    if validType is not None and \
            (not isclass(validType) and \
             not isinstance(validType, Iterable)):
        raise TypeError("validType must be a type or an iterable object.")

    if validType is not None and \
            isinstance(validType, Iterable) and \
            any(not isclass(v) for v in validType):
        raise TypeError("validType items must be types.")

    class _SceneProperty(SceneProperty):
        def __init__(self, *args, **kwargs):
            super().__init__(*args,
                             attribID=ID,
                             validType=validType,
                             **kwargs)

    return _SceneProperty


ScnPropDecorator.attribIDList = list()
ScnPropDecorator.FreeID = 0


class SceneProperty(property):
    _SCM = SceneCallbackManager()
    '''Scene Calback Manager'''

    # !Todo: Sustituir por un inicializador?

    def __init__(self, *args,
                 fpreupdate=None, fpostupdate=None,
                 fvalidtype=None, fvalidvalue=None,
                 attribID=None, validType=None,
                 name=None,
                 **kwargs):
        if SceneProperty._SCM is None:
            raise AttributeError("SceneProperty is not initialized")

        if attribID is None:
            raise AttributeError("attribID must be defined")

        self._attribID = attribID
        self._validType = validType
        if name is None:
            if len(args) > 0:
                self._name = args[0].__name__
            else:
                if 'fget' in kwargs and kwargs['fget'] is not None:
                    self._name = kwargs['fget'].__name__
                elif 'fset' in kwargs and kwargs['fset'] is not None:
                    self._name = kwargs['fset'].__name__
                elif 'fdel' in kwargs and kwargs['fdel'] is not None:
                    self._name = kwargs['fdel'].__name__
                elif 'fpreupdate' in kwargs and kwargs['fpreupdate'] is not None:
                    self._name = kwargs['fpreupdate'].__name__
                elif 'fpostupdate' in kwargs and \
                        kwargs['fpostupdate'] is not None:
                    self._name = kwargs['fpostupdate'].__name__
                elif 'fvalidtype' in kwargs and \
                        kwargs['fvalidtype'] is not None:
                    self._name = kwargs['fvalidtype'].__name__
                elif 'fvalidvalue' in kwargs and \
                        kwargs['fvalidvalue'] is not None:
                    self._name = kwargs['fvalidvalue'].__name__
        else:
            self._name = name

        self.fpreupdate = fpreupdate
        self.fpostupdate = fpostupdate
        self.fvalidtype = fvalidtype
        self.fvalidvalue = fvalidvalue

        if (len(args) > 4): self.fpreupdate = args[4]
        if (len(args) > 5): self.fpostupdate = args[5]
        if (len(args) > 6): self.fvalidtype = args[6]
        if (len(args) > 7): self.fvalidvalue = args[7]
        if (len(args) > 8):
            raise ValueError("SceneProperty takes at most 6 arguments" +
                             "({} given)".format(len(args)))

        #        self._hashId = id(self)

        super().__init__(*(args[0:4]), **kwargs)

    def __set__(self, obj, value):
        if not self.validateType(obj, value):
            raise TypeError("Invalid value type.")

        if not self.validateValue(obj, value):
            raise ValueError("Unexpected value.")

        super().__set__(obj, value)
        self.touch(obj)

    def getter(self, fget):
        return type(self)(
            fget, self.fset, self.fdel, self.__doc__,
            self.fpreupdate, self.fpostupdate,
            self.fvalidtype, self.fvalidvalue,
            name=fget.__name__)

    def setter(self, fset):
        return type(self)(
            self.fget, fset, self.fdel, self.__doc__,
            self.fpreupdate, self.fpostupdate,
            self.fvalidtype, self.fvalidvalue,
            name=fset.__name__)

    def deleter(self, fdel):
        return type(self)(
            self.fget, self.fset, fdel, self.__doc__,
            self.fpreupdate, self.fpostupdate,
            self.fvalidtype, self.fvalidvalue,
            name=fdel.__name__)

    def preupdater(self, fpreupdate):
        return type(self)(
            self.fget, self.fset, self.fdel, self.__doc__,
            fpreupdate, self.fpostupdate,
            self.fvalidtype, self.fvalidvalue,
            name=fpreupdate.__name__)

    def postupdater(self, fpostupdate):
        return type(self)(
            self.fget, self.fset, self.fdel, self.__doc__,
            self.fpreupdate, fpostupdate,
            self.fvalidtype, self.fvalidvalue,
            name=fpostupdate.__name__)

    def typevalidator(self, fvalidtype):
        return type(self)(
            self.fget, self.fset, self.fdel, self.__doc__,
            self.fpreupdate, self.fpostupdate,
            fvalidtype, self.fvalidvalue,
            name=fvalidtype.__name__)

    def valuevalidator(self, fvalidvalue):
        return type(self)(
            self.fget, self.fset, self.fdel, self.__doc__,
            self.fpreupdate, self.fpostupdate,
            self.fvalidtype, fvalidvalue,
            name=fvalidvalue.__name__)

    # =============================================================================
    #  Property functions
    # =============================================================================

    # !todo: No me gusta que le tengas que pasar el objeto    
    def touch(self, obj, **kwargs):
        if self.fpreupdate is not None: self.fpreupdate(obj, **kwargs)
        SceneProperty._SCM.updatedAttrib(attrib=self, obj=obj, **kwargs)
        if self.fpostupdate is not None: self.fpostupdate(obj, **kwargs)

    def getValue(self, obj):
        name = self._name
        if not hasattr(type(obj), name):
            raise ValueError("Class has not ATTR " + name)

        if not isinstance(getattr(type(obj), name), SceneProperty):
            raise TypeError(name, " is not SceneProperty")

        return getattr(obj, name)

    def setValue(self, obj, value):
        name = self._name
        if not hasattr(type(obj), name):
            raise ValueError("Class has not ATTR " + name)

        if not isinstance(getattr(type(obj), name), SceneProperty):
            raise TypeError(name, " is not SceneProperty")

        return setattr(obj, name, value)

    def readOnly(self):
        return self.fset is None

    def getValidType(self):
        return self._validType

    def getID(self):
        return self._attribID

    def getName(self):
        return self._name

    def validateType(self, obj, value):
        if self._validType is not None:
            if isinstance(self._validType, Iterable):
                if not any(isinstance(value, v) for v in self._validType):
                    return False
            elif not isinstance(value, self._validType):
                return False

        if self.fvalidtype is not None and not self.fvalidtype(obj, value):
            return False

        return True

    def validateValue(self, obj, value):
        if self.fvalidvalue is not None:
            return self.fvalidvalue(obj, value)

        return True

    # =============================================================================
    #   Conexion y sesconexion de atributos 
    # =============================================================================   
    def connect2Attrib(self, cb):
        SceneProperty._SCM.connect2Attrib(cb, attrib=self)

    #    def connect2ObjAttrib (self,cb,obj):        
    #        SceneProperty._SCM.connect2ObjAttrib(cb, attrib=self,
    #                                               obj=obj)
    #    
    #    def connect2ClassAttrib(self,cb, objOrClass):
    #        SceneProperty._SCM.connect2ClassAttrib(cb, attrib=self,
    #                                               objOrClass = objOrClass)

    def disconnectFromAttrib(self, cb):
        SceneProperty._SCM.disconnectFromAttrib(cb, attrib=self)

    #    def disconnectFromObjAttrib (self, cb, obj):        
    #        SceneProperty._SCM.disconnectFromObjAttrib(cb, attrib=self,
    #                                               obj=obj)
    #    
    #    def disconnectFromClassAttrib(self, cb, objOrClass):
    #        SceneProperty._SCM.disconnectFromClassAttrib(cb, attrib=self,
    #                                                 objOrClass = objOrClass)

    def removeConnections(self, obj):
        SceneProperty._SCM.removeObjAttribConnections(attrib=self, obj=obj)

    # =============================================================================
    #   Clases internas para indexado  
    # =============================================================================   
    def __hash__(self):
        return hash((self._attribID, self._name))

    #                    self._hashId)

    def __eq__(self, other):
        if isinstance(other, SceneProperty):
            return (self._attribID, self._name) == \
                   (other._attribID, other._name)
        else:
            return False


if __name__ == '__main__':
    class Test:
        def __init__(self):
            self._x = 10

        @ScnPropDecorator()
        def readOnly(self):
            return 1

        @ScnPropDecorator(attribID='x')
        def x(self):
            """I'm the 'x' property."""
            return self._x

        @x.setter
        def x(self, value):
            self._x = value


    t = Test()
    print(t.x)

    print(Test.x.readOnly() is False)
    print(Test.readOnly.readOnly())

    print(Test.x.getValidType())
    print(Test.readOnly.getValidType())

    print(Test.x.getID())
    print(Test.readOnly.getID())

    print(Test.x.validateType(t, 1))
    print(Test.readOnly.validateType(t, 1))

    print(Test.x.validateValue(t, 1))
    print(Test.readOnly.validateValue(t, 1))

    try:
        class Test2:
            @ScnPropDecorator(attribID='x')
            def x(self):
                """I'm the 'x' property."""
                return self._x
    except Exception as e:
        print(e)
    else:
        print('KO')

    from numbers import Number


    class Test3:
        def __init__(self):
            self._x = 10

        @ScnPropDecorator(validType=Number)
        def x(self):
            """I'm the 'x' property."""
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

        @ScnPropDecorator(validType=[Number, str, Test])
        def y(self):
            """I'm the 'x' property."""
            return self._x

        @y.setter
        def y(self, value):
            self._x = value

        @y.typevalidator
        def y(self, value):
            return not isinstance(value, Test)

        @y.valuevalidator
        def y(self, value):
            return value != 0 if isinstance(value, Number) else True


    try:
        class Test4:
            @ScnPropDecorator(validType="a")
            def x(self):
                """I'm the 'x' property."""
                return self._x

    except Exception as e:
        print(e)
    else:
        print('KO')

    try:
        class Test5:
            @ScnPropDecorator(validType=1)
            def x(self):
                """I'm the 'x' property."""
                return self._x

    except Exception as e:
        print(e)
    else:
        print('KO')

    t = Test3()

    try:
        t.x = "pepe"
    except Exception as e:
        print(e)
    else:
        print('KO')

    try:
        t.y = Test3()
    except Exception as e:
        print(e)
    else:
        print('KO')

    #    t.x = 1
    #    print(t.x)
    #    t.y = 1
    #    print(t.y)
    #    t.y = "pepe"
    #    print(t.y)

    print(Test3.x.getValidType())
    print(Test3.y.getValidType())

    print(Test3.x.getID())
    print(Test3.y.getID())

    print(Test3.x.validateType(t, 1))
    print(Test3.y.validateType(t, 1))

    print(Test3.x.validateType(t, "1") is False)
    print(Test3.y.validateType(t, "1"))

    print(Test3.x.validateValue(t, 1))
    print(Test3.y.validateValue(t, 1))

    print(Test3.x.validateType(t, Test()) is False)
    print(Test3.y.validateType(t, Test()) is False)

    print(Test3.y.validateValue(t, 0) is False)
