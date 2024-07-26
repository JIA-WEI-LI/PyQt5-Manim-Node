import os
from enum import Enum
from PyQt5.QtWidgets import QWidget

class BaseStyleSheet:
    def path(self):
        raise NotImplementedError
    
    def apply(self, widget: QWidget):
        """ apply style sheet to widget """
        setStyleSheet(widget, self)

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