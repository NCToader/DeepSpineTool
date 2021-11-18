# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:01:54 2019

@author: URJC
"""
from matplotlib.colors import LinearSegmentedColormap

colorDict = {
    'baseColors': [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    '28': [(0.02352941, 0.58823529, 0.40784314),
           (0.62352941, 0.04313725, 0.39215686),
           (0.44705882, 1., 0.44705882),
           (0.84313725, 0.48627451, 0.86666667),
           (0.78039216, 0.86666667, 0.56862745),
           (0.27058824, 0.3254902, 0.76078431),
           (0.44313725, 0.82745098, 0.95686275),
           (0.14117647, 0.35294118, 0.38431373),
           (0.14117647, 1., 0.80392157),
           (0.64705882, 0.07843137, 0.03529412),
           (0.94509804, 0.79607843, 0.83529412),
           (0.51764706, 0.31764706, 0.27843137),
           (0.74117647, 0.89019608, 0.11372549),
           (0.18039216, 0.18823529, 0.90588235),
           (0.43921569, 0.62352941, 0.05882353),
           (0.96862745, 0.4627451, 0.49019608),
           (0.08235294, 0.71764706, 0.11764706),
           (0.87058824, 0.09803922, 0.96862745),
           (0.95294118, 0.83137255, 0.14901961),
           (1., 0.24313725, 0.71372549),
           (0.58039216, 0.65098039, 0.99215686),
           (0.81568627, 0.49019608, 0.03529412),
           (0.99215686, 0.34901961, 0.09019608)],
    'cmp2': [(0.95, 0.95, 0.95), (0.85, 0.15, 0), (0.8, 0.25, 0), (0, 1, 0)],
    'cmp3': [(0.95, 0.95, 0.95),  # fondo 0 = 0 + 0 i1fondo +i2fondo
             (0.2, 0.2, 0.2),  # 1 = 1 + 0 i1c1+i2fondo ()
             (0.2, 0.2, 0.2),  # 2 = 2 + 0 i1c1+i2fondo
             (0.85, 0.25, 0),  # 3 = 0 +3 i1fondo + i2c1
             (0, 1, 0),  # 4 = 1 +3 i1c1+ i2c1 OK clase 2
             (0.85, 0.85, 0.0),  # 5 = 2 +3 i1c2 + i2c1 Error de clasificación
             (0.85, 0.25, 0),  # 6 = 0 + 6 i1fondo+ i2c2 Falta información
             (0.85, 0.85, 0.0),  # 7 = 1 + 6 i1c1+ i2c2 Error de clasificación
             (0, 0, 1)],  # 7 = 2 + 6 i1c2+ i2c2 OK clase 2
    'white': [(1, 1, 1)],
    'black': [(0, 0, 0)],
    'lightGrey': [(0.95, 0.95, 0.95)],
    'darkGrey': [(0.2, 0.2, 0.2)],
}


def createColorMap(name, colorSet,
                   firstColorList=None,
                   lastColorList=None,
                   nlabels=None,
                   N=None):
    colorSetSize = len(colorSet)
    fc = firstColorList if firstColorList is not None else []
    lc = lastColorList if lastColorList is not None else []

    dec = len(fc) + len(lc)

    nl = colorSetSize + dec if nlabels is None else nlabels
    N = nl if N is None else N

    if (nl > dec):
        colors = (colorSet * ((nl - dec - 1) // colorSetSize + 1))[:nl - dec]
    else:
        colors = []

    colors = (fc + colors + lc)[:nl]

    return LinearSegmentedColormap.from_list(
        name, colors, N=N)
