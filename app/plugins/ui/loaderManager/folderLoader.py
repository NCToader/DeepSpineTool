# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:19:22 2019

@author: Marcos
"""
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
