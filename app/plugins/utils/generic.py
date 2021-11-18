# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:11:08 2019

@author: Marcos
"""
import numpy as np
from inspect import isroutine


class GenericObject(object):
    def __init__(self, **kwargs):
        super(GenericObject, self).__init__(**kwargs)


# devuelve los atributos, quitando protegidos
# vars(o) ---> [n for n in vars(o)]
# o.__dict__  ---> [n for n in o.__dict__]
def getAttribNames(o,
                   showFunc='name',
                   showNone=False,
                   showPrivate=False,
                   showRoutnines=False,
                   shownMagicMethods=False):
    if showFunc == 'type':
        showf = lambda o, n: (n, type(getattr(o, n)).__name__)
    elif showFunc == 'val':
        showf = lambda o, n: (n, getattr(o, n))
    elif showFunc == 'valAndType':
        showf = lambda o, n: (n, getattr(o, n), type(getattr(o, n)).__name__)
    else:
        showf = lambda o, n: n

    condf = lambda o, n: not any(np.logical_or(
        [
            getattr(o, n) is None,
            n[0] == '_',
            isroutine(getattr(o, n)),
            n.startswith('__') and n.endswith('__')
        ], [
            showNone,
            showPrivate,
            showRoutnines,
            shownMagicMethods
        ]))

    return [showf(o, n) for n in dir(o) if condf(o, n)]