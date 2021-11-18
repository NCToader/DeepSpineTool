# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 23:37:31 2019

@author: Marcos García
"""

import numpy as np


def imgRange(img, is3D=True):
    if not isinstance(img, np.ndarray):
        raise TypeError("Numpy array expected")

    c = 1
    if img.ndim < 2 or img.ndim > 4:
        raise ValueError("Image expected")
    elif img.ndim == 2 or (is3D and img.ndim == 3):
        imgmx = img.max()
        imgmn = img.min()
    elif img.ndim == 4 or (not is3D and img.ndim == 3):
        c = img.shape[-1]
        if c > 4:
            raise ValueError("Usupported image format")
        im = img.reshape(-1, c)
        imgmx = im.max(axis=0)
        imgmn = im.min(axis=0)
    else:
        raise ValueError("Usupported image format")

    dtype = img.dtype
    if np.issubdtype(dtype, np.integer):
        info = np.iinfo(dtype)
        if c == 1:
            realmx = info.max
            realmn = info.min
        else:
            realmx = (np.ones(c) * 255).astype(dtype)
            realmn = np.zeros(c, dtype=dtype)

    elif np.issubdtype(dtype, np.floating):
        if c == 1:
            realmx = imgmx if imgmx > 1.0 else 1.0
            realmn = imgmn if imgmn < -1.0 or realmx != 1.0 else -1.0 \
                if imgmn < 0.0 else 0.0
        else:
            realmx = np.ones(c)
            realmn = -np.ones(c) if np.any(imgmn < 0.0) else np.zeros(c)
    else:
        raise TypeError("Usupported image format")

    return realmn, realmx, imgmn, imgmx


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def rgb2grayStack(rgb):
    rgbI = rgb.reshape(-1, rgb.shape[-2], rgb.shape[-1])
    gray = rgb2gray(rgbI)

    return gray.reshape(rgb.shape[0:len(rgb.shape) - 1])


def multiChannel2SingleChannel(mcImg, channel=0):
    imgT = mcImg.reshape(-1, mcImg.shape[-1])
    scImg = imgT[:, channel]

    return scImg.reshape(mcImg.shape[0:len(mcImg.shape) - 1])


def getAABBImg(img):
    '''
    mxAABBpixel + 1    
    '''
    nzElments = np.nonzero(img)
    mxAABB = np.max(nzElments, axis=1)
    mxAABB += np.ones(mxAABB.shape, dtype=np.int)
    mnAABB = np.min(nzElments, axis=1)

    return mnAABB, mxAABB


def idxAABB(mn, mx):
    return tuple(slice(i, j) for i, j in zip(mn, mx))


def ellipStruct(shape):
    struct = np.zeros(2 * shape + 1)
    index = np.indices(2 * shape + 1)

    center = np.ones(index.shape)
    center = (center.T * shape).T
    mask = ((index - center) ** 2 / (center + 0.001) ** 2).sum(axis=0) <= 1
    struct[mask] = 1

    return struct.astype(np.bool)
