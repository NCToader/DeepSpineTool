# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:33:23 2019

@author: Marcos
#!todo:control de errores
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

class CBSetManager():
    def __init__(self):
        self._cbSet = set()

    def registerCB(self, cb):
        self._cbSet.add(cb)

    def unregisterCB(self, cb):
        self._cbSet.remove(cb)

    def call(self, *args, **kwargs):
        for cb in self._cbSet:
            cb(*args, **kwargs)


class CBDictManager():
    def __init__(self):
        self._cbDict = dict()

    def registerCB(self, key, cb):
        if key not in self._cbDict: self._cbDict[key] = set()
        self._cbDict[key].add(cb)

    def unregisterCB(self, key, cb):
        d = self._cbDict.get(key)
        if d is not None: self._cbDict[key].remove(cb)

    def call(self, key, *args, **kwargs):
        if key not in self._cbDict: return

        for cb in self._cbDict[key]:
            cb(*args, **kwargs)

    def removeKey(self, key):
        if key not in self._cbDict: return

        del self._cbDict[key]
