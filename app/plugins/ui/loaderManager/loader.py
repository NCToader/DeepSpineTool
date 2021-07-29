# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:20:43 2019

@author: Marcos

!todo: controlar que no se cree más de un loader por tipo
"""

from abc import ABC, abstractstaticmethod


class Loader(ABC):
    def __init__(self, prePath):
        self._prePath = prePath
        if not hasattr(self, '_menuPath'):
            raise AttributeError("_menuPath is not defined")
        if not hasattr(self, '_name'):
            raise AttributeError("_name is not defined")

    @property
    def name(self):
        return self._name

    @property
    def menuPath(self):
        if self._prePath is None and self._menuPath is None: return None
        mp = [""] if self._prePath is None else self._prePath
        return mp + self._menuPath if self._menuPath is not None else mp

    @property
    def prefix(self):
        return '/'.join(self.menuPath)

    @property
    def key(self):
        return '/'.join([self.prefix, self.name])

    @property
    def cb(self):
        return type(self)._cb

    @abstractstaticmethod
    def _cb():
        pass

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, Loader):
            return self.key == other.key
        else:
            return False
