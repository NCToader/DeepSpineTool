# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:51:33 2019

@author: URJC
https://gist.github.com/dunossauro/f86c2578fe31c4495f35c3fdaf7585bb
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
"""


class SingletonDecorator:
    def __init__(self, class_):
        self._class_ = class_
        self._instance = None

    def __call__(self, *args, **kwds):
        if self._instance == None:
            self._instance = self._class_(*args, **kwds)
        return self._instance
