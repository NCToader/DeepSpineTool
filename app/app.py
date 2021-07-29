# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:21:10 2019

@author: Marcos

https://docs.python.org/3/faq/windows.html#is-a-pyd-file-the-same-as-a-dll
https://github.com/ContinuumIO/anaconda-issues/issues/10949

"""

from PyQt5 import Qt
from app.core.ui.mainWindow import MainWindow

from app.core.utils import StdoutManager, OutFileStream  # , OutNullStream

from app.plugins.ui import sceneManagerUi as smui

from app.plugins.ui import nodeViewer as nvui

from app.plugins.ui.image.viewer import img3Viewer as i3vui
from app.plugins.ui.image.viewer import img3MultiProjViewer as i3mpvui
from app.plugins.ui.image.editor import roiSelector as rs
from app.plugins.ui.image.editor import marchingCubes as mc
from app.plugins.ui.image.editor import img3MultiProjEditor as i3mpeui
from app.plugins.ui.image.segmentation import segmentationConnector as sc
from app.plugins.ui.saverManager import saverManager as SM
from app.plugins.ui.image import segmentation as sgui
from app.plugins.utils.image import segmentation as sg
from app.plugins.ui.vtkViewer import vtkViewer as vtk
from app.plugins.ui.image.segmentation import segmentationComparator as segComp
from app.plugins.ui.image.segmentation import noiseFilter as nFilt

def run():
    import sys

    # =============================================================================
    #  Inicialización del sistema de log
    # =============================================================================
    logFile = open("qttool.log", "w")
    ofsout = OutFileStream(logFile, out=StdoutManager().consolestdout)
    ofserr = OutFileStream(logFile, out=StdoutManager().consolestderr)
    StdoutManager().defaultstdout = ofsout
    StdoutManager().defaultstderr = ofserr
    StdoutManager().pushStdout(ofsout)
    StdoutManager().pushStderr(ofserr)
    #    StdoutManager().verbose = False
    #    StdoutManager().allowForcePrint = True
    StdoutManager().tfverbose = False
    #    StdoutManager().pushStderr(OutNullStream())
    #    StdoutManager().pushStdout(OutNullStream())

    # =============================================================================
    #  Inicialización de la ventana principal
    # =============================================================================
    app = Qt.QApplication(sys.argv)
    mw = MainWindow(title="Spine Segmentation Tool")

    # =============================================================================
    # Inicialización de las extensiones
    # =============================================================================
    smui.init()
    nvui.init()
    i3vui.init()
    i3mpvui.init()
    i3mpeui.init()
    rs.init()
    sc.init()
    SM.init()
    vtk.init()
    mc.init()
    segComp.init()
    nFilt.init()

    sg.initUnet
    sgui.initCNDL()

    # =============================================================================
    #  Ventana principal
    # =============================================================================
    mw.createWindowMenu()
    mw.show()
    try:
        sys.exit(app.exec())
    except Exception as err:
        raise err
    finally:
        StdoutManager().popStdout()
        StdoutManager().popStderr()
        logFile.close()


if __name__ == '__main__':
    run()
