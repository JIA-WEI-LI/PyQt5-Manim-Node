import math

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import QLine

from config.icon import Icon
from config.palette import WindowColor

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200 ,200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 創建圖像場景
        self.graphicsScene = NodeGraphicsScene()

        # 創建圖像視圖
        self.view = QGraphicsView(self)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)

        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

class NodeGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gridSize = 20
        self.sceenWidth, self.sceenHeight = 640000, 640000
        self.setSceneRect(self.sceenWidth//2, self.sceenHeight//2, self.sceenWidth, self.sceenHeight)

        self.penLight = QPen(WindowColor.DEFAULT_PEN_LIGHT)
        self.penLight.setWidth(1)
        self.setBackgroundBrush(WindowColor.DEFAULT_BACKGROUND)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left))
        right = int(math.floor(rect.right))
        top = int(math.floor(rect.top))
        bottom= int(math.floor(rect.bottom))

        lines_light = []

        painter.setPen(self.penLight)
        painter.drawLines(*lines_light)