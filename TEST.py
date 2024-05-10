import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QPainterPath
from PyQt5.QtCore import QRectF


class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Color Picker')

        self.color = QColor(255, 0, 0)  # 初始顏色為紅色

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 繪製彩色選擇器
        for x in range(self.width()):
            for y in range(self.height()):
                hue = (360 - (360 * (x / self.width()))) / 360.0
                saturation = y / self.height()
                color = QColor.fromHsvF(hue, saturation, 1.0)
                painter.setPen(color)
                painter.drawPoint(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        # 在點擊處取得顏色
        self.color = self.pickColor(event.pos())
        print("Selected color:", self.color.getRgb())

    def pickColor(self, pos):
        hue = (360 - (360 * (pos.x() / self.width()))) / 360.0
        saturation = pos.y() / self.height()
        return QColor.fromHsvF(hue, saturation, 1.0)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 定義邊緣圓角半徑
        radius = 10
        
        # 繪製彩色選擇器
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        painter.setClipPath(path)
        for x in range(self.width()):
            for y in range(self.height()):
                hue = (360 - (360 * (x / self.width()))) / 360.0
                saturation = y / self.height()
                color = QColor.fromHsvF(hue, saturation, 1.0)
                painter.setPen(color)
                painter.drawPoint(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec_())
