# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:20:17 2019

@author: Marcos
"""
from app.plugins.ui.loaderManager import FolderLoader
from app.plugins.ui.loaderManager import BasicTiffLoader
from app.plugins.ui.loaderManager import MeshLoader

basicLoaders = [FolderLoader, BasicTiffLoader, MeshLoader]
