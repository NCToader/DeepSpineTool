# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 16:20:20 2019

@author: Marcos
"""
import numpy as np
from enum import IntEnum
# from numbers import Number

from app.core.model import SceneNode
from app.core.model.sceneProperty import ScnPropDecorator


class Image(SceneNode):
    class Channels(IntEnum):
        R = 1
        RG = 2
        RGB = 3
        RGBA = 4

    class Dims(IntEnum):
        img2D = 2
        img3D = 3

    def __init__(self, name=None):
        super().__init__(name)

        self._img = None
        self._nChannels = None
        self._nDims = None

    @ScnPropDecorator("Image.img", validType=np.ndarray)
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        #        if isinstance(value, np.ndarray):
        size = value.shape
        sizeLen = len(size)
        channels = size[-1]

        oldChannels = self._nChannels
        oldDims = self._nDims
        odlDT = self.channelDType
        oldBPC = self.bytesPerChannel

        #            if sizeLen > 4:
        #                raise ValueError("Error: 4 is the " +
        #                                 "maximun number of " +
        #                                 "dimensions allowed.")
        #            if sizeLen < 2:
        #                raise ValueError("Error: 2 is the " +
        #                                 "minimun number of " +
        #                                 "dimensions allowed.")

        if sizeLen == 4:
            #                if channels > 4:
            #                    raise ValueError("Error: 4 is the " +
            #                                     "maximun number of " +
            #                                     "components allowed.")
            #                else:
            self._nChannels = self.getClass().Channels(channels)
            self._nDims = self.getClass().Dims.img3D

        elif sizeLen == 3:
            if channels < 4 and self._nDims == self.getClass().Dims.img2D:
                self._nChannels = self.getClass().Channels(channels)
                self._nDims = self.getClass().Dims.img2D
            else:
                self._nChannels = self.getClass().Channels.R
                self._nDims = self.getClass().Dims.img3D

        else:
            self._nChannels = self.getClass().Channels.R
            self._nDims = self.getClass().Dims.img2D

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

    #        else:
    #            raise TypeError("Error: ndarray expected")

    @img.valuevalidator
    def img(self, value):
        size = value.shape
        sizeLen = len(value.shape)
        if 4 < sizeLen or 2 > sizeLen: return False
        channels = size[-1]
        if 4 == sizeLen and channels > 4: return False
        return True

    @ScnPropDecorator("Image.nDims", validType=[Dims, int])
    def nDims(self):
        return self._nDims

    @nDims.setter
    def nDims(self, value):
        #        if not isinstance(value,self.getClass().Dims):
        #            raise TypeError("Error: Image.Dim expected")
        #        if self._img is None:
        #            raise ValueError("Error: Image is not initialized")

        size = self._img.shape
        sizeLen = len(size)

        oldChannels = self._nChannels

        #        if sizeLen == 4:
        #            if v != 3:
        #                raise ValueError("Error: Img and nDim are not compatible")
        if sizeLen == 3:
            if value == 3:
                self._nDims = self.getClass().Dims.img3D
                self._nChannels = self.getClass().Channels(1)
            else:
                self._nDims = self.getClass().Dims.img2D
                self._nChannels = self.getClass().Channels(size[-1])
        #        else:
        #            if v != 2:
        #                raise ValueError("Error: Img and nDim are not compatible")

        if oldChannels != self._nChannels:
            self.getClass().nChannels.touch(self)

    @nDims.valuevalidator
    def nDims(self, value):
        if self._img is None: return False
        if value != 2 and value != 3: return False
        sizeLen = len(self._img.shape)
        if sizeLen == 4 and value != 3: return False
        if sizeLen == 2 and value != 2: return False
        if sizeLen == 3 and value == 2: return self._img.shape[-1] <= 4
        return True

    @ScnPropDecorator("Image.nChannels", validType=[Channels, int])
    def nChannels(self):
        return self._nChannels

    @ScnPropDecorator("Image.bytesPerChannel", validType=int)
    def bytesPerChannel(self):
        return self._img.dtype.itemsize if self._img is not None \
            else None

    @ScnPropDecorator("Image.channelDType", validType=[type, str])
    def channelDType(self):
        return self._img.dtype if self._img is not None \
            else None

    @channelDType.setter
    def channelDType(self, value):
        #        try:
        #            t = np.dtype (value)
        t = np.dtype(value)
        #        except:
        #            raise TypeError("Error: Numpy.DType expected")
        #
        #        if self._img is None:
        #            raise ValueError("Error: Image is not initialized")

        odlDT = self.channelDType
        oldBPC = self.bytesPerChannel

        self._img = self._img.astype(t)

        if odlDT != self.channelDType:
            self.getClass().img.touch(self)
            self.getClass().channelType.touch(self)

            if oldBPC != self.bytesPerChannel:
                self.getClass().bytesPerChannel.touch(self)

    @channelDType.valuevalidator
    def channelDType(self, value):
        try:
            np.dtype(value)
        except:
            return False

        if self._img is None:
            return False

        return True

    @ScnPropDecorator("Image.channelType", validType=str)
    def channelType(self):
        return self._img.dtype.name if self._img is not None \
            else None
