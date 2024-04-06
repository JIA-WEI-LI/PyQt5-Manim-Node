from PyQt5.QtWidgets import QApplication, QProgressBar
from PyQt5.QtGui import QCursor, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt

class ProgressBar(QProgressBar):
    '''自定義點擊式按鈕'''
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        # 滑鼠點擊時，更新進度
        if event.buttons() == Qt.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.updateProgress(event)

    def mouseMoveEvent(self, event):
        # 滑鼠移動時，如果正在拖動，更新進度
        if hasattr(self, 'dragging') and self.dragging:
            self.updateProgress(event)

    def mouseReleaseEvent(self, event):
        # 釋放滑鼠後，停止拖動
        if hasattr(self, 'dragging') and self.dragging:
            del self.dragging

    def updateProgress(self, event):
        mouse_x = event.x()
        total_width = self.width()
        progress = (mouse_x / total_width) * 100
        self.setValue(progress)