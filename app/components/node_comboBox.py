from PyQt5.QtWidgets import QApplication, QComboBox, QWidget
from PyQt5.QtGui import QCursor, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet

class ComboBox(QComboBox):
    '''自定義下拉式選單'''
    def __init__(self, items=["List 1", "List 2", "List 3"], parent=None):
        super(ComboBox, self).__init__(parent=parent)