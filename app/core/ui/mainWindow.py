# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:34:24 2019

@author: URJC

#todo: Meter excepciones
#!todo: Advance docking https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System
"""

from PyQt5 import Qt, QtCore
from enum import Enum
import copy

from app.core.utils import SingletonDecorator
from app.core import model as sc
from app.core.ui.processingDialog import ProcessingDialog


class DockAreaId(Enum):
    Top = Qt.Qt.TopDockWidgetArea
    Bottom = Qt.Qt.BottomDockWidgetArea
    Right = Qt.Qt.RightDockWidgetArea
    Left = Qt.Qt.LeftDockWidgetArea


@SingletonDecorator
class MainWindow(Qt.QMainWindow):
    def __init__(self, parent=None, title=None):
        Qt.QMainWindow.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self._actions = dict()

        self._initMenu()

        self._initDock()

        self._initCentralWidget()

        self._windowMenu = None
        self._dockOptionMenu = None
        self._activeWindowMenu = None

        if title is not None:
            if not isinstance(title, str):
                raise TypeError("String expected")
            self.setWindowTitle(title)

    # =============================================================================
    #   Funciones de inicialización
    # =============================================================================

    def _initMenu(self):
        self._menus = dict()
        _menuBar = self.menuBar()
        _menuBar.setNativeMenuBar(False)
        self._menus[None] = _menuBar

        self.addAction("&New", shortcut=(QtCore.Qt.Key_N | QtCore.Qt.CTRL))
        self.addAction("&Load", shortcut=(QtCore.Qt.Key_L | QtCore.Qt.CTRL))
        self.addAction("&Save", shortcut=(QtCore.Qt.Key_S | QtCore.Qt.CTRL))
        self.addAction("&Quit", shortcut=(QtCore.Qt.Key_Q | QtCore.Qt.CTRL))

        self.addAction2Menu("&New", ["Scene"])
        self.addAction2Menu("&Load", ["Scene"])
        self.addAction2Menu("&Save", ["Scene"])
        self.addAction2Menu("&Quit", ["Scene"])

        def newScene():
            ok = self.confirmMsg("Are you sure you want to create a new Scene?",
                                 info="Any unsaved changes will be lost")

            if ok: sc.Scene().new()

        def loadScene():
            ok = self.confirmMsg("Are you sure you want to load a Scene?",
                                 info="Any unsaved changes will be lost")
            if ok:
                fn = self.loadFileDialog(filters=["Scene (*.scn)",
                                                  "All Files (*)"])

                if fn is not None:

                    def load():
                        if not sc.Scene().loadz(fn[0]):
                            raise IOError(fn[0])

                    if not self.processDialog(cb=load, isICB=False,
                                              wtitle="Loading...",
                                              title="Loading scene...",
                                              closeOnFinished=True,
                                              hideConsole=True):
                        self.warningMsg("The scene file cannot be opened")

        def saveScene():
            fn = self.saveFileDialog(filters=["Scene (*.scn)",
                                              "All Files (*)"])

            if fn is not None:
                def save():
                    if not sc.Scene().savez(fn[0]):
                        raise IOError(fn[0])

                if not self.processDialog(cb=save, isICB=False,
                                          wtitle="Saving...",
                                          title="Saving scene...",
                                          closeOnFinished=True,
                                          hideConsole=True):
                    self.warningMsg("The scene file cannot be writte")

        self.addActionCB("&New", newScene)
        self.addActionCB("&Load", loadScene)
        self.addActionCB("&Save", saveScene)
        self.addActionCB("&Quit", self.close)

    def _initDock(self):
        self.setDockOptions(self.dockOptions() |
                            Qt.QMainWindow.AllowNestedDocks |
                            Qt.QMainWindow.GroupedDragging)
        self._docks = []

        self.setStyleSheet('''QMainWindow::separator {
                    		background: rgb(100, 100, 100);
                    		width: 4px;
                    		height: 4px;}''')

    #        self.setStyleSheet('''QDockWidget {padding-left: 10px;
    #                                           padding-right: 10px;
    #                                           border-style: outset;
    #                                           border-width: 4px;
    #                                           border-color: black;}''')
    #                 border: 10px solid lightgray; background: black}''')

    def _initCentralWidget(self):
        self._centralWidget = Qt.QTabWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.hide()
        self._tabs = []

    # =============================================================================
    # Gestión de acciones y menus
    # =============================================================================

    def createWindowMenu(self, menuPath=None, mainWindowConfig=True):
        if menuPath is not None:
            if not isinstance(menuPath, str):
                if not isinstance(menuPath, list) or \
                        all(isinstance(i, str) for i in menuPath):
                    raise TypeError("String or list of strings expected")
                else:
                    mp = menuPath
            else:
                mp = [menuPath]
        else:
            mp = ["Window"]

        # ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        pf = "_&%234&&_"
        self._pf = pf

        self._windowMenu = self.createMenu(menuPath=mp)
        self._activeWindowMenu = self.createPopupMenu()

        action = self._windowMenu.addMenu(self._activeWindowMenu)
        action.setText("Active Windows")

        if mainWindowConfig:
            self._windowMenu.addSeparator()
            mp.append("Dock Options")
            self._dockOptionMenu = self.createMenu(menuPath=mp)

            def setOptions():
                if self._dockOptionMenu is None: return

                opts = Qt.QMainWindow.DockOption(0)
                actions = self._dockOptionMenu.actions()
                optsList = (Qt.QMainWindow.AnimatedDocks,
                            Qt.QMainWindow.AllowNestedDocks,
                            Qt.QMainWindow.AllowTabbedDocks,
                            Qt.QMainWindow.ForceTabbedDocks,
                            Qt.QMainWindow.VerticalTabs,
                            Qt.QMainWindow.GroupedDragging)

                for a, o in zip(actions, optsList):
                    if a.isChecked(): opts = opts | o

                self.setDockOptions(opts)

            def addAction(name, prop):
                action = self.addAction(name, prefix=pf)
                self.addAction2Menu(name, menuPath=mp, prefix=pf)
                action.setCheckable(True);
                action.setChecked(self.dockOptions() & prop)
                self.addActionCB(name, setOptions, prefix=pf)

            addAction("Animated docks", Qt.QMainWindow.AnimatedDocks)
            addAction("Allow nested docks", Qt.QMainWindow.AllowNestedDocks)
            addAction("Allow tabbed docks", Qt.QMainWindow.AllowTabbedDocks)
            addAction("Force tabbed docks", Qt.QMainWindow.ForceTabbedDocks)
            addAction("Top tabs", Qt.QMainWindow.VerticalTabs)
            addAction("Grouped dragging", Qt.QMainWindow.GroupedDragging)

    def addAction(self, name, prefix=None, icon=None, shortcut=None):
        key = prefix + name if prefix is not None else name

        entry = self._actions.get(key)
        if entry is None:
            action = Qt.QAction(self)
            action.setText(name)

            entry = {'action': action, 'triggerCBs': None}

            def func():
                cb = self._actions[key]['triggerCBs']
                if cb is not None:
                    cb()

            setattr(self, "_" + key, Qt.pyqtSlot()(func))
            action.triggered.connect(getattr(self, "_" + key))
            #            action.toggled.connect(getattr(self,"_"+key))

            self._actions[key] = entry

        else:
            action = entry['action']

        if icon is not None:
            action.setIcon(icon)

        if shortcut is not None:
            action.setShortcut(shortcut)

        self._actions[key]['action'] = action

        return action

    def addActionCB(self, name, cb, prefix=None):
        key = prefix + name if prefix is not None else name
        if (self._actions.get(key)) is None: return None

        entry = self._actions[key]
        entry['triggerCBs'] = cb

        return entry['action']

    def getMenu(self, menuPath=None):
        if menuPath is None:
            return self._menus.get(None)
        else:
            self._menus.get(tuple(menuPath))

    def createMenu(self, menuPath=None):
        if menuPath is None: menuPath = list()
        menu = None

        stack = copy.copy(menuPath)
        toCreate = list()

        for i in range(len(menuPath)):
            menu = self._menus.get(tuple(stack))
            if menu is not None:
                break

            toCreate.append(stack.pop(-1))

        if menu is None:
            menu = self._menus.get(None)

        toCreate.reverse()
        for item in toCreate:
            stack.append(item)
            menu = menu.addMenu(item)
            self._menus[tuple(stack)] = menu

        return menu

    def addAction2Menu(self, name, menuPath=None, prefix=None):
        key = prefix + name if prefix is not None else name
        if (self._actions.get(key)) is None: return

        menu = self.createMenu(menuPath=menuPath)
        menu.addAction(self._actions[key]['action'])

    #    def addAction2Toolbar(name,toolbarName):
    #        pass
    #

    # =============================================================================
    #   Ventanas modales
    # =============================================================================
    @staticmethod
    def warningMsg(msg):
        # !todo: Asegurar que se borran al concluir sin llamar a deleteLater
        # https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
        msgBox = Qt.QMessageBox()
        msgBox.setText(msg)
        msgBox.setWindowTitle("Warning")
        msgBox.setIcon(Qt.QMessageBox.Warning)
        msgBox.setWindowFlags(msgBox.windowFlags() &
                              ~Qt.Qt.WindowCloseButtonHint)
        return msgBox.exec()

    @staticmethod
    def confirmMsg(question, info=None):
        msgBox = Qt.QMessageBox()
        msgBox.setText(question)
        msgBox.setInformativeText(info)
        msgBox.setWindowTitle("Please, confirm operation")
        msgBox.setIcon(Qt.QMessageBox.Question)
        msgBox.setWindowFlags(msgBox.windowFlags() &
                              ~Qt.Qt.WindowCloseButtonHint)
        msgBox.setStandardButtons(Qt.QMessageBox.Ok | Qt.QMessageBox.Cancel)
        msgBox.setEscapeButton(Qt.QMessageBox.Cancel)
        msgBox.setDefaultButton(Qt.QMessageBox.Cancel)

        return msgBox.exec() == Qt.QMessageBox.Ok

    @staticmethod
    def processDialog(cb,
                      isICB,
                      wtitle=None,
                      title=None,
                      iconNum=1,
                      finishMsg=None,
                      terminateMsg=None,
                      closeOnFinished=True,
                      closeButtonEnabled=True,
                      hideConsole=False,
                      hideProgressBar=False):

        w = ProcessingDialog(title=title, iconNum=iconNum)
        w.setWindowTitle(wtitle)
        w.closeOnFinished = closeOnFinished
        w.closeButtonEnabled = closeButtonEnabled
        w.hideConsole = hideConsole
        w.hideProgressBar = hideProgressBar

        if finishMsg is not None:
            w.finishMsg = finishMsg
        else:
            w.finishMsg = \
                """
                #################################
                ## Finalizado
                #################################
                """

        if terminateMsg is not None:
            w.terminateMsg = terminateMsg
        else:
            w.terminateMsg = \
                """
                #################################
                ## Terminate
                #################################
                """

        if isICB:
            r = w.execICB(cb)
        else:
            r = w.execCB(cb)

        return r == Qt.QDialog.Accepted

    @staticmethod
    def loadFileDialog(filters=None, dir_=None, title="Please, select a valid file"):
        dialog = Qt.QFileDialog()
        dialog.setWindowTitle(title)
        dialog.setFileMode(Qt.QFileDialog.ExistingFile)
        dialog.setAcceptMode(Qt.QFileDialog.AcceptOpen)

        if dir_ is None: dir_ = "."
        dialog.setDirectory(dir_)

        if filters is not None:
            dialog.setNameFilters(filters)

        if dialog.exec():
            fileName = dialog.selectedFiles()
            if (len(fileName) == 0):
                return None
            else:
                return fileName
        else:
            return None

    @staticmethod
    def saveFileDialog(filters=None, dir_=None):
        dialog = Qt.QFileDialog()
        dialog.setWindowTitle("Please, select a file")
        dialog.setFileMode(Qt.QFileDialog.AnyFile)
        dialog.setAcceptMode(Qt.QFileDialog.AcceptSave)

        if dir_ is None: dir_ = "."
        dialog.setDirectory(dir_)

        if filters is not None:
            dialog.setNameFilters(filters)

        if dialog.exec():
            fileName = dialog.selectedFiles()
            if (len(fileName) == 0):
                return None
            else:
                return fileName
        else:
            return None

    @staticmethod
    def saveDirectoryDialog(dir_=None):
        dialog = Qt.QFileDialog()

        if dir_ is None: dir_ = "."
        dialog.setDirectory(dir_)

        fileName = dialog.getExistingDirectory()
        if (len(fileName) == 0):
            return None
        else:
            return fileName

    # =============================================================================
    #      Gestión de ventanas
    # =============================================================================

    def createDockableWidget(self, widget, title, dockAreaId=None,
                             hideOnClose=True):

        if dockAreaId is None:
            dockAreaId = DockAreaId.Right

        dock = Qt.QDockWidget(title, self)

        # !todo: is really necesary
        widget.setParent(dock)
        dock.setWidget(widget)
        dock.setFloating(False)
        self._docks.append(dock)

        nfound = True
        for d in self._docks:
            if self.dockWidgetArea(d) == dockAreaId.value:
                dock.show()
                self.tabifyDockWidget(d, dock)

                nfound = False
                break

        if nfound: self.addDockWidget(dockAreaId.value, dock)

        if self._activeWindowMenu is not None:
            actions = self.createPopupMenu().actions()
            for a in actions:
                self._activeWindowMenu.addAction(a)

        if not hideOnClose:
            #            dock.setAttribute(Qt.Qt.WA_DeleteOnClose)
            def closeButtonClk(bool):

                ok = self.confirmMsg(
                    "Do you really want to close this window?\n" +
                    "Unsaved changes will be lost")

                if ok:
                    dock.hide()
                    #dock.setAttribute(Qt.Qt.WA_DeleteOnClose)
                    dock.close()
                else:
                    dock.show()

            b = dock.findChildren(Qt.QAbstractButton,
                                  "qt_dockwidget_closebutton")[0]
            b.clicked.connect(copy.copy(closeButtonClk))

        return dock

    def createCentralTab(self, widget, title, icon=None):
        self._tabs.append(widget)
        return self._centralWidget.addTab(widget, title)


if __name__ == '__main__':
    import sys
    import time

    app = Qt.QApplication(sys.argv)
    ex = MainWindow()
    ex2 = MainWindow()  # prueba singleton

    for i in range(3):
        listWidget = Qt.QListWidget()
        listWidget.addItem("item1")
        listWidget.addItem("item2")
        listWidget.addItem("item3")

        ex.createDockableWidget(listWidget, "R" + str(i))

    for i in range(3):
        listWidget = Qt.QListWidget()
        listWidget.addItem("item1")
        listWidget.addItem("item2")
        listWidget.addItem("item3")
        ex2.createDockableWidget(listWidget, "L" + str(i),
                                 dockAreaId=DockAreaId.Left)
    for i in range(3):
        listWidget = Qt.QListWidget()
        listWidget.addItem("item1")
        listWidget.addItem("item2")
        listWidget.addItem("item3")
        ex2.createCentralTab(listWidget, "C" + str(i))

    ex.show()


    def test():
        for i in range(10):
            yield i * 10
            print(i)
            time.sleep(1)


    print(ex.processDialog(test,
                           True,
                           wtitle=None,
                           title=None,
                           iconNum=1,
                           finishMsg=None,
                           terminateMsg=None,
                           closeOnFinished=False,
                           closeButtonEnabled=True,
                           hideConsole=False,
                           hideProgressBar=False))

    sys.exit(app.exec())
