# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:24:48 2019

@author: URJC

https://pypi.org/project/tifffile/
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

import tifffile as tiff
# import inspect as ins
from app.plugins.utils.inspectors.classInspector import getClassAttribs


def getTiffMetadata(tif):
    return _checkTypeNExe(tif, _getTiffMetadata)


def getAdditionalInformation(tif):
    return _checkTypeNExe(tif, _getAdditionalInformation)


def getTiffInfoStr(tif):
    return _checkTypeNExe(tif, _getTiffInfoStr)


def getBooleans(tif):
    return _checkTypeNExe(tif, _getBooleans)


def _getTiffInfoStr(tif):
    def printHeader(title):
        return '{:*^80}\n*  '.format('') + title + '\n{:*^80}\n'.format('')

    result = ""

    result = result + printHeader("Summary") + str(tif) + '\n\n'

    result = result + printHeader("Known Metadata Types")
    varl = getTiffMetadata(tif)

    for v in varl:
        result = result + " - " + "{:14}".format(v[0] + ':')
        if v[1] is None:
            result = result + " None \n"
        else:
            result = result + "\n"
            for k in v[1]:
                result = result + "{:5}".format(" * ") + "" + str(k) \
                         + "{:3}".format(":") \
                         + str(v[1][k]) + "\n"

    result = result + printHeader("Series" + str(len(tif.series))) + '\n'

    varl = getClassAttribs(tif.series[0],  # notHas = 'parent',
                           notStartsWith='_')
    for v in varl:
        result = result + " - " \
                 + "{:14}".format(v[0] + ':') + str(v[1]) + '\n'

    result = result + printHeader("Pages" + str(len(tif.pages))) + '\n'

    varl = getClassAttribs(tif.pages[0],  # notHas = 'parent',
                           notStartsWith='_')
    for v in varl:
        result = result + " - " \
                 + "{:14}".format(v[0] + ':') + str(v[1]) + '\n'

    result = result + printHeader("Aditional Information")
    varl = getAdditionalInformation(tif)

    for v in varl:
        result = result + " - " \
                 + "{:14}".format(v[0] + ':') + str(v[1]) + '\n'

    result = result + printHeader("Booleans")
    varl = getBooleans(tif)

    for v in varl:
        result = result + " - " \
                 + "{:14}".format(v[0] + ':') + str(v[1]) + '\n'

    result = result + printHeader("Doc Strings")
    result = result + str(tif.__doc__) + '\n'
    result = result + str(tif.series[0].__doc__) + '\n'
    result = result + str(tif.pages[0].__doc__) + '\n'

    return result


def _checkTypeNExe(tif, func):
    if isinstance(tif, str):
        try:
            with tiff.TiffFile(tif) as tif:
                result = func(tif)
        except:
            result = None
        return result

    elif isinstance(tif, tiff.TiffFile):
        return func(tif)

    else:
        raise TypeError("Parameter type not allowed")


def _getTiffMetadata(tif):
    res = getClassAttribs(tif, endsWith='_metadata')

    res = list(map(lambda x: (x[0].replace('_metadata', ''), x[1]), res))
    return res


def _getAdditionalInformation(tif):
    res = getClassAttribs(tif, notEndsWith='_metadata',
                          notStartsWith=('is', '_'),
                          notHas=("pages", "series", "filehandle"))
    return res


def _getBooleans(tif):
    res = getClassAttribs(tif, startsWith=('is'))
    return res
