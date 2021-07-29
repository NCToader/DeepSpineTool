# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:33:23 2019

@author: Marcos
#!todo:control de errores
"""


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
