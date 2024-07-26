import os
from typing import Union
from enum import Enum
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QFile

def getStyleSheetFromFile(file: Union[str, QFile]):
    """ get style sheet from qss file """
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding='utf-8')
    f.close()
    return qss

class BaseStyleSheet:
    def path(self):
        raise NotImplementedError
    
    def apply(self, widget: QWidget):
        """ apply style sheet to widget """
        setStyleSheet(widget, self)

    def content(self):
        return getStyleSheetFromFile(self.path())

    def setPath(self, custom_path:str):
        self.custom_path = custom_path

class StyleSheet(BaseStyleSheet, Enum):
    EMPTY = "empty"
    EDIORTWINDOW = "editor_window"
    NODECONTENT = "node_content"
    
    def path(self):
        if hasattr(self, 'custom_path'):
            return self.custom_path
        return f"nodeeditor\\resources\\style\\{self.value}.qss"
    
class BlenderStyleSheet(BaseStyleSheet, Enum):
    BUTTON = "button"
    LINEEDIT = "lineedit"
    COLORDIALOG = "colordialog"
    COLOR_DIALOG = "color_dialog"
    
    def path(self):
        return f"nodeeditor\\BlenderWidget\\style\\{self.value}.qss"
    
def setStyleSheet(widget: QWidget, stylesheet: 'BaseStyleSheet'):
    """ Helper function to set the style sheet to the widget """
    qss_path = stylesheet.path()
    if os.path.exists(qss_path):
        with open(qss_path, 'r', encoding='utf-8') as file:
            qss_text = file.read()
            widget.setStyleSheet(qss_text)
            return qss_text
    else:
        raise FileNotFoundError(f"QSS file not found: {qss_path}")