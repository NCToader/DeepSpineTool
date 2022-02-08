# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:20:43 2019

@author: Marcos

!todo: controlar que no se cree más de un loader por tipo
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
