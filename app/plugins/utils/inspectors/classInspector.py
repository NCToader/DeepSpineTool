# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:24:19 2019

@author: URJC
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

import inspect as ins
from app.core.model import SceneProperty
from app.core.model import SceneNode


def getClassAttribs(clssOrObj,
                    startsWith=None, endsWith=None,
                    notStartsWith=None, notEndsWith=None,
                    startsNEndsWith=None, notStartsNEndsWith=None,
                    has=None, notHas=None):
    attr = ins.getmembers(clssOrObj, lambda a: not (ins.isroutine(a)))

    return _getClassAttribs(attr,
                            startsWith, endsWith, notStartsWith, notEndsWith,
                            startsNEndsWith, notStartsNEndsWith, has, notHas)


def getClassSCPAttribs(clssOrObj,
                       startsWith=None, endsWith=None,
                       notStartsWith=None, notEndsWith=None,
                       startsNEndsWith=None, notStartsNEndsWith=None,
                       has=None, notHas=None):
    clss = type(clssOrObj) if isinstance(clssOrObj, SceneNode) else clssOrObj
    if not issubclass(clss, SceneNode): raise TypeError("SceneNode expected")

    attr = ins.getmembers(clss, lambda a: isinstance(a, SceneProperty))

    return _getClassAttribs(attr,
                            startsWith, endsWith, notStartsWith, notEndsWith,
                            startsNEndsWith, notStartsNEndsWith, has, notHas)


def _getClassAttribs(attr,
                     startsWith=None, endsWith=None,
                     notStartsWith=None, notEndsWith=None,
                     startsNEndsWith=None, notStartsNEndsWith=None,
                     has=None, notHas=None):
    def createCond(cond, f):
        def TrueF(*args):
            return True

        if cond is None:
            return TrueF
        else:
            return f

    swc = createCond(startsWith, lambda x: x.startswith(startsWith))
    ewc = createCond(endsWith, lambda x: x.endswith(endsWith))

    nswc = createCond(notStartsWith,
                      lambda x: not x.startswith(notStartsWith))
    newc = createCond(notEndsWith, lambda x: not x.endswith(notEndsWith))

    sewc = createCond(startsNEndsWith,
                      lambda x: \
                          any(x.startswith(y[0]) and x.endswith(y[1]) \
                              for y in tuple(startsNEndsWith)))
    nsewc = createCond(notStartsNEndsWith,
                       lambda x: \
                           not any(x.startswith(y[0]) and x.endswith(y[1]) \
                                   for y in tuple(notStartsNEndsWith)))

    hc = createCond(has, lambda x: any(y in x for y in tuple(has)))
    nhc = createCond(notHas, lambda x: not any(y in x for y in tuple(notHas)))

    rslt = [a for a in attr if swc(a[0]) and ewc(a[0]) and nswc(a[0]) and \
            newc(a[0]) and sewc(a[0]) and nsewc(a[0]) and hc(a[0]) and nhc(a[0])]

    return rslt
