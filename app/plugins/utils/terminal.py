# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:17:43 2019

@author: Marcos
"""
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
