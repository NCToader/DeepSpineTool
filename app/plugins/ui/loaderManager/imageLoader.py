# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:21:34 2019

@author: Marcos
https://pypi.org/project/tifffile/
https://programtalk.com/python-examples/skimage.external.tifffile.TiffFile/

https://www.scivision.dev/writing-multipage-tiff-with-python/
https://github.com/scivision/pyimagevideo
https://github.com/libvips/libvips/issues/1253

import tifffile
with tifffile.TiffFile('file.tif') as tif:
    tif_tags = {}
    for tag in tif.pages[0].tags.values():
        name, value = tag.name, tag.value
        tif_tags[name] = value
    image = tif.pages[0].asarray()
"""
import traceback

import tifffile as tiff

from app.core.ui.mainWindow import MainWindow

from app.plugins.ui.loaderManager import Loader
from app.plugins.utils.inspectors.tiffInspector import getTiffInfoStr
from app.plugins.model.image import Image


class BasicTiffLoader(Loader):

    def __init__(self, *args):
        self._menuPath = ["Image"]
        self._name = "Basic Tiff Loader (2D/3D)"
        super().__init__(*args)

    @classmethod
    def _cb(clss):
        fn = MainWindow().loadFileDialog(filters=["Tiff (*.tif)",
                                                  "All Files (*)"])

        result = list()

        if fn is not None:
            try:
                with tiff.TiffFile(fn[0]) as tif:
                    unsupported = list()
                    idxList = list()
                    try:
                        print(getTiffInfoStr(tif))
                    except:
                        print("TiffInfo cannot be read.")

                    for i, s in enumerate(tif.series):
                        print(s.ndim, s.axes)
                        if s.ndim == 2 and all(x in s.axes for x in ('X', 'Y')):
                            idata = s.asarray()
                            xpos = s.axes.find('X')
                            ypos = s.axes.find('Y')
                            idata = idata.transpose((ypos, xpos))
                            img = Image()
                            img.img = idata
                            img.nDims = Image.Dims.img2D
                            result.append(img)
                            idxList.append(i)

                        elif s.ndim == 3 and \
                                all(x in s.axes for x in ('X', 'Y', 'Z')):

                            idata = s.asarray()
                            xpos = s.axes.find('X')
                            ypos = s.axes.find('Y')
                            zpos = s.axes.find('Z')
                            idata = idata.transpose((zpos, ypos, xpos))
                            img = Image()
                            img.img = idata
                            img.nDims = Image.Dims.img3D
                            result.append(img)
                            idxList.append(i)

                        elif s.ndim == 3 and \
                                all(x in s.axes for x in ('X', 'Y', 'Q')):

                            idata = s.asarray()
                            xpos = s.axes.find('X')
                            ypos = s.axes.find('Y')
                            zpos = s.axes.find('Q')
                            idata = idata.transpose((zpos, ypos, xpos))
                            img = Image()
                            img.img = idata
                            img.nDims = Image.Dims.img3D
                            result.append(img)
                            idxList.append(i)

                        elif s.ndim == 3 and \
                                all(x in s.axes for x in ('X', 'Y')):

                            idata = s.asarray()
                            xpos = s.axes.find('X')
                            ypos = s.axes.find('Y')
                            cpos = (i for i, x in enumerate(s.axes) \
                                    if any(y == x for y in ('X', 'Y')))[0]
                            idata = idata.transpose((ypos, xpos, cpos))
                            img = Image()
                            img.img = idata
                            img.nDims = Image.Dims.img2D

                            if idata.shape[-1] < 4:
                                result.append(img)
                                idxList.append(i)
                            else:
                                unsupported.append(i)

                        elif s.ndim == 4 and \
                                all(x in s.axes for x in ('X', 'Y', 'Z')):

                            idata = s.asarray()
                            xpos = s.axes.find('X')
                            ypos = s.axes.find('Y')
                            zpos = s.axes.find('Z')

                            cpos = [i for i, x in enumerate(s.axes) \
                                    if not any(x == y for y in ('X', 'Y', 'Z'))][0]

                            idata = idata.transpose((zpos, ypos, xpos, cpos))

                            img = Image()
                            img.img = idata
                            img.nDims = Image.Dims.img3D
                            if idata.shape[-1] < 4:
                                result.append(img)
                                idxList.append(i)
                            else:
                                unsupported.append(i)
                    if len(result) == 0:
                        MainWindow().warningMsg(
                            "The image file format is not supported.")
                    elif len(result) > 0:
                        if len(unsupported) > 1:
                            MainWindow().warningMsg(
                                "The format of series:" + str(unsupported)
                                + "are not supported.")
                        if len(result) == 1:
                            result[0].name = tif.filename
                        else:
                            for i, r in zip(idxList, result):
                                r.name = 'Serie_' + str(i)


            except Exception as e:
                print(e)
                traceback.print_exc()
                MainWindow().warningMsg("The image file cannot be opened")

        return result


if __name__ == '__main__':
    BasicTiffLoader
