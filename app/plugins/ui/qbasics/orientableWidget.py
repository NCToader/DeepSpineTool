## -*- coding: utf-8 -*-
# """
# Created on Fri Nov 15 17:34:30 2019
#
# @author: URJC
# """
#
# from PyQt5 import Qt
# from enum import Enum, auto
#
# class OrientableWidget(Qt.QWidget):
#    class Orientation(Enum):
#        Horizontal          = auto()
#        VerticalTopToBottom = auto()
#        VerticalBottomToTop = auto()
#                
#    def __init__(self, *args, orientation = Orientation.Horizontal, **kwargs):
#        super().__init__(*args,**kwargas)
#        self._orientation = orientation
#        
#    @property
#    def orientation(self):
#        return self._orientation
#    
#    @orientation.setter
#    def orientation(self, value):
#        self._orientation = value
#    
#    def sizeHint(self):
#        sh = super().sizeHint()
#        if (self._orientation != Horizontal): sh.transpose()
#        return sh
#    
#            
#    def paintEvent(event):
#         painter = Qt.QStylePainter(self)
#         option = QStyleOptionButton() XXXXXX
#         self.initStyleOption(option)
#
#        if self._orientation  ==  \
#           OrientableWidget.Orientation.VerticalTopToBottom:
#                painter.rotate(90)
#                painter.translate(0, -1 * self.width())
#                option.rect = option.rect.transposed()
#
#        elif self._orientation  ==  \
#           OrientableWidget.Orientation.VerticalBottomToTop:
#                painter.rotate(-90)
#                painter.translate(-1 * height(), 0)
#                option.rect = option.rect.transposed()
#
#        painter.drawControl(QStyle::CE_PushButton, option) XXXX
#
#
# if __name__ == '__main__':
#    import sys
##    import numpy as np
#    
#    app = Qt.QApplication(sys.argv)
#    ex = ColapsableWidget()
#    ex.show()
#    Qt.QPushButton("B1",ex)
#    
#
#    sys.exit(app.exec())
