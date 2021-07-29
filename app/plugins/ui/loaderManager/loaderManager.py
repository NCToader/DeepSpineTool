# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:19:29 2019

@author: URJC
"""
import copy
# from PyQt5 import Qt

from app.core.utils import SingletonDecorator
from app.core import ui as mw

from app.plugins.ui.loaderManager import Loader, basicLoaders


@SingletonDecorator
class LoaderManager:
    defaultLoaderList = basicLoaders

    # !todo: No tiene mucho sentido meter parametros si no controlas cuando se
    #       inicializán los módulos
    def __init__(self,
                 prePath=None, loadersList=None, defaultLoaders=True):
        self._createNodeCB = None
        self._prePath = ["Add Node"] if prePath is None else prePath
        self._menuRoot = mw.MainWindow().createMenu(menuPath=self._prePath)
        self._registeredLoaders = dict()

        loadersList = loadersList if loadersList is not None \
            else self.defaultLoaderList

        self._initDefaultLoaders(loadersList)

    def _initDefaultLoaders(self, loadersList):
        for l in loadersList:
            self.registerLoader(l(self._prePath))

    @property
    def createNodeCB(self):
        return self._createNodeCB

    @createNodeCB.setter
    def createNodeCB(self, value):
        if not callable(value):
            raise TypeError("{} is not callable".format(value))
        self._createNodeCB = value

    @property
    def menu(self):
        return self._menuRoot

    @property
    def registeredLoaders(self):
        return self._registeredLoaders.values()

    def isRegisteredLoader(self, loader):
        return loader.key

    def registerLoader(self, loader):
        if not isinstance(loader, Loader):
            raise TypeError("can only register Loader not {}".format(
                type(Loader)))

        name = loader.name
        cb = loader.cb
        menuPath = loader.menuPath
        prefix = loader.prefix
        key = loader.key

        if key in self._registeredLoaders: return
        self._registeredLoaders[key] = loader

        def func():
            if self._createNodeCB is not None:
                self._createNodeCB(cb)

        MW = mw.MainWindow()
        MW.addAction(name, prefix=prefix)
        MW.addActionCB(name, copy.copy(func), prefix=prefix)
        MW.addAction2Menu(name, menuPath=menuPath, prefix=prefix)
