from app.core.utils import SingletonDecorator
from app.plugins.ui.saverManager import basicSavers, Saver
from app.core import ui as mw

@SingletonDecorator
class SaverManager:
    defaultSaverList = basicSavers

    def __init__(self, saversList=None, defaultSavers=True):
        saversList = saversList if saversList is not None \
            else self.defaultSaverList
        self._prePath=['Savers']
        self._initDefaultSavers(saversList)

    def _initDefaultSavers(self, saversList):
        for s in saversList:
            self.initSaver(s(self._prePath))

    def initSaver(self, saver):
        if not isinstance(saver, Saver):
            raise TypeError('can only register Saver not {}'.format(type(Saver)))
        name = saver.name
        cb = saver.cb
        menuPath = saver.menuPath
        prefix = saver.prefix
        MW = mw.MainWindow()
        MW.addAction(name, prefix=prefix)
        MW.addActionCB(name,cb, prefix=prefix)
        MW.addAction2Menu(name, menuPath=menuPath, prefix=prefix)

def init():
    SaverManager()