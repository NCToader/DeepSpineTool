# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:51:33 2019

@author: URJC
https://gist.github.com/dunossauro/f86c2578fe31c4495f35c3fdaf7585bb
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
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

class SingletonDecorator:
    def __init__(self, class_):
        self._class_ = class_
        self._instance = None

    def __call__(self, *args, **kwds):
        if self._instance == None:
            self._instance = self._class_(*args, **kwds)
        return self._instance
