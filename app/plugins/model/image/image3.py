# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 16:20:38 2019

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


class Image3(Image):
    @Image.img.valuevalidator
    def img(self, value):
        size = value.shape
        sizeLen = len(value.shape)
        if 4 < sizeLen or 3 > sizeLen: return False
        channels = size[-1]
        if 4 == sizeLen and channels > 4: return False
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

        if sizeLen == 4:
            self._nChannels = self.getClass().Channels(channels)
            self._nDims = self.getClass().Dims.img3D

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
        if value != 2 and value != 3: return False
        sizeLen = len(self._img.shape)
        if sizeLen == 4 and value != 3: return False
        if sizeLen == 2 and value != 2: return False
        return True

#    @Image.img.setter
#    def img(self,value):
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
#            if sizeLen > 4:
#                raise ValueError("Error: 4 is the" + 
#                                 "maximun number of" +
#                                 "dimensions allowed.")
#            if sizeLen < 3:
#                raise ValueError("Error (Image2): 2 is the" + 
#                                 "minimun number of" +
#                                 "dimensions allowed.")
#            
#            if sizeLen == 4:
#                if channels > 4:
#                    raise ValueError("Error: 4 is the" + 
#                                     "maximun number of" +
#                                     "components allowed.")
#                else:
#                    self._nChannels = self.getClass().Channels(channels)
#                    self._nDims = self.getClass().Dims.img3D
#                    
#            else: 
#                    self._nChannels = self.getClass().Channels.R
#                    self._nDims = self.getClass().Dims.img3D 
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
#        if value != self.getClass().Dims.img3D:
#            raise ValueError("Error(Image3): Image.Dims.img3D" +
#                             "is the only value allowed")
