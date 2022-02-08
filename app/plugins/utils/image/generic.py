# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:11:08 2019

@author: Marcos
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

import numpy as np
from inspect import isroutine


class GenericObject():
    def __init__(self, **kwargs):
        # super(GenericObject, self).__init__()
        self.__dict__.update(**kwargs)


class ObjPool():
    def __init__(self, obj, objInc=1, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._obj = obj
        self._objList = []
        self._objInc = objInc

        self._incPool()

    def incPool(self):
        self._objList += [self._obj(*self._args, **self._kwargs)] * self._objInc

    def getObj(self):
        if len(self._objList) > 0:
            return self._objList.pop()
        else:
            self._objList += [] * self.objInc
            return self._objList.pop()

    def releaseObj(self, obj):
        self._objList.append(obj)


# devuelve los atributos, quitando protegidos
# vars(o) ---> [n for n in vars(o)]
# o.__dict__  ---> [n for n in o.__dict__]
def getAttribNames(o,
                   showFunc='name',
                   showNone=False,
                   showPrivate=False,
                   showRoutnines=False,
                   shownMagicMethods=False):
    if showFunc == 'type':
        showf = lambda o, n: (n, type(getattr(o, n)).__name__)
    elif showFunc == 'val':
        showf = lambda o, n: (n, getattr(o, n))
    elif showFunc == 'valAndType':
        showf = lambda o, n: (n, getattr(o, n), type(getattr(o, n)).__name__)
    else:
        showf = lambda o, n: n

    condf = lambda o, n: not any(np.logical_or(
        [
            getattr(o, n) is None,
            n[0] == '_',
            isroutine(getattr(o, n)),
            n.startswith('__') and n.endswith('__')
        ], [
            showNone,
            showPrivate,
            showRoutnines,
            shownMagicMethods
        ]))

    return [showf(o, n) for n in dir(o) if condf(o, n)]


def isIterable(obj):
    'Indica si es una lista o una tupla'
    return isinstance(obj, list) or isinstance(obj, tuple)
#    return isinstance(obj, (list, tuple))




