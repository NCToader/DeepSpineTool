pyrcc5 -o XXXXXX.py XXXXX.qrc
pyrcc5 -o icons_rc.py 00icons.qrc
python -m PyQt5.uic.pyuic -x 000processing.ui -o ui_Processing.py
pause