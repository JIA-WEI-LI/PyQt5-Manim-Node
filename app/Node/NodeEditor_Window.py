import math

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon, QMouseEvent, QPainter, QPen
from PyQt5.QtCore import QLine, Qt, QEvent

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
        self.view = NodeGraphicsView(self.graphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

class NodeGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gridSize = 20
        self.gridSquare = 5
        self.sceenWidth, self.sceenHeight = 640000, 640000
        self.setSceneRect(self.sceenWidth//2, self.sceenHeight//2, self.sceenWidth, self.sceenHeight)

        self.penLight = QPen(WindowColor.DEFAULT_PEN_LIGHT)
        self.penLight.setWidth(1)
        self.penDark = QPen(WindowColor.DEFAULT_PEN_DARK)
        self.penDark.setWidth(2)
        self.setBackgroundBrush(WindowColor.DEFAULT_BACKGROUND)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        # 創造網格背景
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom= int(math.ceil(rect.bottom()))

        firstLeft = left - (left % self.gridSize)
        firstTop = top - (top % self.gridSize)

        lines_light, lines_dark = [], []
        for x in range(firstLeft, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquare) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))
        for y in range(firstTop, bottom, self.gridSize):
            if (y % (self.gridSize * self.gridSquare) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))

        painter.setPen(self.penLight)
        painter.drawLines(*lines_light)
        painter.setPen(self.penDark)
        painter.drawLines(*lines_dark)

class NodeGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initUI()
        self.setScene(self.graphicsScene)

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        '''滑鼠點擊事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        '''滑鼠放開事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠中鍵'''
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)

    def middleMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠中鍵'''
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.MouseButton.LeftButton, event.buttons() & -Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)