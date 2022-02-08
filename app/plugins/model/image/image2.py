# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 16:21:05 2019

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

from app.plugins.model.image.image import Image
import numpy as np


class Image2(Image):
    @Image.img.valuevalidator
    def img(self, value):
        size = value.shape
        sizeLen = len(value.shape)
        if 3 < sizeLen or 2 > sizeLen: return False
        channels = size[-1]
        if 3 == sizeLen and channels > 4: return False
        return True

    @img.setter
    def img(self, value):
        size = value.shape
        sizeLen = len(size)
        channels = size[-1]

        oldChannels = self._nChannels
        oldDims = self._nDims
        odlDT = self.channelDType
        oldBPC = self.bytesPerChannel

        if sizeLen == 3:
            self._nDims == self.getClass().Dims.img2D
            self._nChannels = self.getClass().Channels(channels)
        else:
            self._nChannels = self.getClass().Channels.R
            self._nDims = self.getClass().Dims.img3D

        self._img = value

        if oldChannels != self._nChannels:
            self.getClass().nChannels.touch(self)
        if oldDims != self._nDims:
            self.getClass().nDims.touch(self)
        if odlDT != self.channelDType:
            self.getClass().channelDType.touch(self)
            self.getClass().channelType.touch(self)
        if oldBPC != self.bytesPerChannel:
            self.getClass().bytesPerChannel.touch(self)

    @Image.nDims.valuevalidator
    def nDims(self, value):
        if self._img is None: return False
        if value != 2: return False
        return True


#    @Image.img.setter
#    def img(self,value):
#        
#        if isinstance(value, np.ndarray):
#            size     = value.shape
#            sizeLen  = len(size)
#            channels = size[-1]
#            
#            oldChannels = self._nChannels
#            oldDims = self._nDims
#            odlDT = self.channelDType
#            oldBPC = self.bytesPerChannel
#            
#            if sizeLen > 3:
#                raise ValueError("Error (Image2): 3 is the " + 
#                                 "maximun number of" +
#                                 "dimensions allowed.")
#            if sizeLen < 2:
#                raise ValueError("Error: 2 is the " + 
#                                 "minimun number of " +
#                                 "dimensions allowed.")
#                    
#            if sizeLen == 3: 
#                if channels < 4:
#                    self._nDims == self.getClass().Dims.img2D
#                    self._nChannels = self.getClass().Channels(channels)
#                else:
#                    raise ValueError("Error(Image2): 4 is the " + 
#                                     "maximun number of " +
#                                     "components allowed.")
#            else:
#                 self._nChannels = self.getClass().Channels.R
#                 self._nDims = self.getClass().Dims.img3D
#                 
#        
#            self._img = value
#            
#            if oldChannels != self._nChannels: 
#                self.getClass().nChannels.touch(self)
#            if oldDims != self._nDims: 
#                self.getClass().nDims.touch(self)
#            if odlDT != self.channelDType:
#                self.getClass().channelDType.touch(self)
#                self.getClass().channelType.touch(self)
#            if oldBPC != self.bytesPerChannel:
#                self.getClass().bytesPerChannel.touch(self)
#        else:
#            raise TypeError("Error: ndarray expected")
#    
#    @Image.nDims.setter
#    def nDims (self, value):
#        if not isinstance(value,self.getClass().Dims):
#            raise TypeError("Error: Image.Dim expected")
#        
#        if self._img is None:
#            raise ValueError("Error: Image is not initialized")
#        
#        if value != self.getClass().Dims.img2D:
#            raise ValueError("Error(Image2): Image.Dims.img2D " +
#                             "is the only value allowed")


if __name__ == '__main__':
    def printImg(img):
        #        print ("IMG ", img.img)
        print()
        print("NDims ", img.nDims)
        print("NChannels ", img.nChannels)
        print("ChannelDType ", img.channelDType)
        print("ChannelType ", img.channelType)


    def occCB(obj=None, attrib=None, **kwarg):

        print("#############################################################")
        print("occCB: ")
        print("#############################################################")
        print(obj.name)
        print(attrib.__get__(obj))
        print(**kwarg)


    img = Image("1")
    printImg(img)

    img2 = Image2("2")
    printImg(img2)

    img2.img = np.arange(10 * 10 * 3).reshape(10, 10, 3)
    printImg(img2)

    try:
        img2.img = np.arange(10 * 10 * 5).reshape(10, 10, 5)
    except Exception as e:
        print('OK', e)

    try:
        img2.nDims = Image.Dims.img3D
    except Exception as e:
        print('OK', e)

    Image.img.connect2Attrib(occCB)

    img2.img = np.arange(5 * 10 * 3).reshape(5, 10, 3)
    img.img = np.arange(5 * 10 * 3).reshape(5, 10, 3)

    Image.img.disconnectFromAttrib(occCB)

    Image2.img.connect2Attrib(occCB)

    img2.img = np.arange(5 * 10).reshape(5, 10)
    img.img = np.arange(5 * 10 * 3).reshape(5, 10, 3)

    Image2.img.disconnectFromAttrib(occCB)
