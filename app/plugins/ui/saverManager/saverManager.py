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