from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QCursor, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt

class PushButton(QPushButton):
    '''自定義點擊式按鈕'''
    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, event: QPaintEvent) -> None:
        '''鼠標進入按紐'''
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def leaveEvent(self, event: QMouseEvent) -> None:
        '''鼠標離開按紐'''
        QApplication.restoreOverrideCursor()