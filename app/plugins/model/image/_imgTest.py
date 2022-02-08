# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:46:29 2019

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

from app.plugins.model.image.image import Image
import numpy as np

if __name__ == '__main__':
    def printImg(img):
        #        print ("IMG ", img.img)
        print()
        print("NDims ", img.nDims)
        print("NChannels ", img.nChannels)
        print("ChannelDType ", img.channelDType)
        print("ChannelType ", img.channelType)


    img = Image()
    printImg(img)

    try:
        img.nDims = Image.Dims.img3D
    except Exception as e:
        print('OK', e)

    try:
        img.channelDType = 'u1'
    except Exception as e:
        print('OK', e)

    try:
        img.nDims = 0
    except Exception as e:
        print('OK', e)

    try:
        img.channelDType = 'eoeo'
    except Exception as e:
        print('OK', e)

    i = np.arange(10 * 10 * 3).reshape(10, 10, 3)
    img.img = i
    printImg(img)

    img.nDims = Image.Dims.img3D
    printImg(img)
    img.nDims = Image.Dims.img2D
    printImg(img)

    img.channelDType = np.byte
    printImg(img)

    img.channelDType = 'u2'
    printImg(img)

    img.img = i
    printImg(img)

    img.nDims = Image.Dims.img3D
    img.img = i
    printImg(img)

    i = np.arange(10 * 10 * 10 * 2).reshape(10, 10, 10, 2)
    img.img = i
    printImg(img)

    img.nDims = Image.Dims.img3D
    printImg(img)
    try:
        img.nDims = Image.Dims.img2D
    except Exception as e:
        print('OK', e)

    try:
        i = np.arange(10 * 10 * 10 * 5).reshape(10, 10, 10, 5)
        img.img = i
    except Exception as e:
        print('OK', e)

    try:
        i = np.arange(10 * 10 * 10 * 4).reshape(10, 10, 10, 2, 2)
        img.img = i
    except Exception as e:
        print('OK', e)

    try:
        i = np.arange(10).reshape(10)
        img.img = i
    except Exception as e:
        print('OK', e)

    i = np.arange(10 * 10).reshape(10, 10)
    img.img = i
    printImg(img)

    img.nDims = Image.Dims.img2D
    printImg(img)
    try:
        img.nDims = Image.Dims.img3D
    except Exception as e:
        print('OK', e)
