# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:17:43 2019

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

import subprocess as sp


def clc():
    sp.os.system("cls" if sp.os.name == 'nt' else 'clear')


def clearv():
    for name in dir():
        if not name.startswith('_'):
            del globals()[name]

    for name in dir():
        if not name.startswith('_'):
            del locals()[name]
