# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:17:43 2019

@author: Marcos
"""

import matplotlib.pyplot as plt
from skimage import measure as ms
import numpy as np
from os.path import join
from app.plugins.utils.terminal import clearv
from app.plugins.utils.generic import GenericObject

# limpia las variables del entorno
clearv()

Dx = 0.0751562
Dy = 0.0751562
Dz = 0.279911

DrawSpine = None
showPlots = True

PATH = './data/if6.1.2-3enero'
gtName = 'gt_ub'
pdName = 'pd_ub'

class spinesSegmentationPairing():
    def __init__(self, predictionImg, gtImg):
        self.pdSpineImg = predictionImg
        self.gtSpineImg = gtImg
        assert self.gtSpineImg.shape == self.pdSpineImg.shape
        w, h, d = self.gtSpineImg.shape
        # pdSpineImg = pdSpineImgList[0]
        # gtSpineImg = gtSpineImgList[0]

        # =============================================================================
        # Binarización
        # =============================================================================
        gtSpinesBin = self.pdSpineImg > 150
        pdSpinesBin = self.gtSpineImg > 150

        if showPlots:
            plt.figure()
            plt.imshow(np.max(gtSpinesBin, axis=0))
            plt.figure()
            plt.imshow(np.max(pdSpinesBin, axis=0))

        # =============================================================================
        # Conectividad
        # =============================================================================
        # http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_label.html
        # http://cs-tklab.na-inet.jp/~tkouya/python/scipy-lectures/packages/scikit-image/index.html
        gtSpinesLabel = ms.label(gtSpinesBin, background=0, connectivity=3)
        pdSpinesLabel = ms.label(pdSpinesBin, background=0, connectivity=3)

        print("Número de etiquetas ground truth ", gtSpinesLabel.max())
        print("Número de etiquetas predicción ", pdSpinesLabel.max())

        if showPlots:
            plt.figure()
            plt.imshow(np.max(gtSpinesLabel, axis=0))
            plt.figure()
            plt.imshow(np.max(pdSpinesLabel, axis=0))

        gtSpines = getConnectedComponentInfo(gtSpinesLabel,
                                             attr=[('neighbor', dict())])
        pdSpines = getConnectedComponentInfo(pdSpinesLabel,
                                             attr=[('neighbor', dict())])

        # !todo, se puede acelerar
        # =============================================================================
        # Detectando solapes (opcion 1)
        # =============================================================================
        print("Detectando solapes", flush=True)
        # !todo, se puede acelerar
        for gt, pd in zip(gtSpinesLabel.ravel(), pdSpinesLabel.ravel()):
            if not (pd == 0 or gt == 0):
                gtIdx = gt - 1
                pdIdx = pd - 1

                gtn = gtSpines[gtIdx].neighbor
                if pdIdx not in gtn:
                    a = GenericObject()
                    a.overlap = 0
                    gtn[pdIdx] = a

                pdn = pdSpines[pdIdx].neighbor
                if gtIdx not in pdn:
                    a = GenericObject()
                    a.overlap = 0
                    pdn[gtIdx] = a

                gtn[pdIdx].overlap += 1
                pdn[gtIdx].overlap += 1

            # !todo, se puede acelerar

        print("Solapes de la predicción", flush=True)
        for pd in pdSpines:
            print(len(pd.neighbor), end=' ')
            for n in pd.neighbor:
                print(" ", n, end=' ')
            print("")

        print("Solapes del GT", flush=True)
        for gt in gtSpines:
            print(len(gt.neighbor), end=' ')
            for n in gt.neighbor:
                print(" ", n, " ", gt.neighbor[n].overlap, end=' ')
            print("")

        # =============================================================================
        # Calculando nuevas etiquetas
        # =============================================================================
        print("Calculando nuevas etiquetas", flush=True)
        gtNewLabel, pdNewLabel, lsize = relabelOverlaped(gtSpines, pdSpines, getSize=True)

        print(gtNewLabel, pdNewLabel)

        # pdNewLabel, gtNewLabel = relabelOverlaped (pdSpines, gtSpines)
        # print (gtNewLabel, pdNewLabel)

        relabel(pdSpinesLabel, pdNewLabel)
        relabel(gtSpinesLabel, gtNewLabel)

        if showPlots:
            plt.figure()
            plt.imshow(np.max(gtSpinesLabel, axis=0))
            plt.figure()
            plt.imshow(np.max(pdSpinesLabel, axis=0))
            plt.show()

def getConnectedComponentInfo(labelIMG, bbox=True, coords=True,
                              label=True, npixels=True,
                              attr=None):
    propList = ms.regionprops(labelIMG)

    size = len(propList)
    infoList = [GenericObject() for _ in range(size)]

    for i in range(size):
        prop = propList[i]
        a = infoList[i]
        if bbox:    a.bbox = np.array(prop.bbox)
        if coords:  a.coords = np.array(prop.coords)
        if label:   a.labelID = (prop.label - 1)
        if npixels: a.npixels = prop.area

        if attr is not None:
            for x, y in attr:
                setattr(a, x, y.copy())

    return infoList


def relabelOverlaped(labels1, labels2,
                     overlapRatio=0, joinAll=True, getSize=False):
    l1size = len(labels1)
    l2size = len(labels2)
    newLabels1 = np.array([-1] * l1size)
    newLabels2 = np.array([-1] * l2size)

    currentLabel = -1;

    if not joinAll:
        for i in range(l1size):
            if (newLabels1[i] == -1) and (len(labels1[i].neighbor) > 0):
                currentLabel += 1
                newLabels1[i] = currentLabel

                for nb1 in labels1[i].neighbor:
                    overlap = labels1[i].neighbor[nb1].overlap

                    # todo: Comprobar esta condición. Debería quedarse
                    # con el mayor solape
                    if (labels2[nb1].npixels / overlap >= overlapRatio):
                        newLabels2[nb1] = currentLabel

    else:
        for i in range(l1size):
            if len(labels1[i].neighbor) > 0:
                if newLabels1[i] == -1:
                    currentLabel += 1
                    clbl = currentLabel
                    newLabels1[i] = clbl
                else:
                    clbl = newLabels1[i]

                npixels1 = labels1[i].npixels

                for nb1 in labels1[i].neighbor:
                    overlap = labels1[i].neighbor[nb1].overlap
                    npixels2 = labels2[nb1].npixels

                    if (npixels2 / overlap >= overlapRatio or
                            npixels1 / overlap >= overlapRatio):

                        newLabels2[nb1] = clbl

                        for nb2 in labels2[nb1].neighbor:
                            overlap = labels2[nb1].neighbor[nb2].overlap
                            if (npixels2 / overlap >= overlapRatio or
                                    labels1[nb2].npixels / overlap >= overlapRatio):
                                newLabels1[nb2] = clbl

    l1upaired = currentLabel + 1
    for i in range(l1size):
        if len(labels1[i].neighbor) == 0:
            currentLabel += 1
            newLabels1[i] = currentLabel

    l2upaired = currentLabel + 1
    for i in range(l2size):
        if len(labels2[i].neighbor) == 0:
            currentLabel += 1
            newLabels2[i] = currentLabel

    lmax = currentLabel + 1

    return (newLabels1, newLabels2, (l1upaired, l2upaired, lmax)) if (getSize) else (newLabels1, newLabels2)


def relabel(labelIMG, newLabels):
    for i, j, k in np.ndindex(labelIMG.shape):
        oldLabel = labelIMG[i, j, k] - 1

        if oldLabel >= 0:
            labelIMG[i, j, k] = newLabels[oldLabel] + 1


#    tmp = np.zeros (gtSpineImg.shape)
#    for i in range(len(newLabels)):
#        tmp += (labelIMG == i+1)*(newLabels[i]+1)


# def main():
# =============================================================================
# Carga de datos
# =============================================================================
# gtSpinesFileName, gtSpineImgList = load_tiff_from_folder(
#     path=PATH, filt=gtName, ext='tif')
# pdSpinesFileName, pdSpineImgList = load_tiff_from_folder(
#     path=PATH, filt=pdName, ext='tif')


