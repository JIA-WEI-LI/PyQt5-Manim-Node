import math

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon, QMouseEvent, QPainter, QPen, QWheelEvent
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

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10  # 調整初始值
        self.zoomStep = 1
        self.zoomRange = [0, 5]

        self.dragStartPosition = None  # 滑鼠開始拖曳位置

        # 事件篩選器
        self.installEventFilter(self)

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        '''滑鼠點擊事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        '''滑鼠放開事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠中鍵'''
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.dragStartPosition = event.pos()

    def middleMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠中鍵'''
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.dragStartPosition = None

    def leftMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠左鍵'''
        return super().mousePressEvent(event)
        
    def rightMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠右鍵'''
        return super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠左鍵'''
        return super().mouseReleaseEvent(event)
    
    def rightMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠右鍵'''
        return super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        '''滑鼠中鍵滾論縮放視窗'''
        zoomOutFactor = 1 / self.zoomInFactor
        oldPos = self.mapToScene(event.pos())
        
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
            
        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
            
        if not clamped or self.zoomClamp is False:    
            self.scale(zoomFactor, zoomFactor)

    def mouseMoveEvent(self, event: QMouseEvent):
        '''滑鼠移動事件'''
        if self.dragStartPosition:
            delta = event.pos() - self.dragStartPosition
            self.dragStartPosition = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def eventFilter(self, obj, event: QMouseEvent):
        '''事件篩選器'''
        if event.type() == QEvent.Type.MouseButtonPress:
            print("Mouse Pressed:", event.button())
        elif event.type() == QEvent.Type.MouseButtonRelease:
            print("Mouse Released:", event.button())
        return super().eventFilter(obj, event)
