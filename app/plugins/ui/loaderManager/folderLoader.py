# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:19:22 2019

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

from app.plugins.ui.loaderManager import Loader
from app.plugins.model.folder import Folder


class FolderLoader(Loader):

    def __init__(self, *args):
        self._menuPath = None
        self._name = "Folder"
        super().__init__(*args)

    @staticmethod
    def _cb():
        return [Folder("Folder")]
