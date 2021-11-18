python -m PyQt5.uic.pyuic -x text.ui -o ui_text.py
python -m PyQt5.uic.pyuic -x SceneManagerTree.ui -o ui_SceneManagerTree.py
pyrcc5 -o coreResource.py core_resource.qrc
pyrcc5 -o iconResources.py iconResources.qrc
pause