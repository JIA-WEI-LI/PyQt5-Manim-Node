from PyQt5.QtWidgets import QApplication, QProgressBar
from PyQt5.QtGui import QCursor, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt

class ProgressBar(QProgressBar):
    '''自定義點擊式按鈕'''
    def __init__(self, parent=None):
        super().__init__(parent)