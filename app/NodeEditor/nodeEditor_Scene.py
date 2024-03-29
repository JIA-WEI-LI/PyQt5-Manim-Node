import math

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QLine

from config.palette import WindowColor

class Scene:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.sceneWidth, self.sceneHeight = 64000, 64000
        
        self.__initUI()
        
    def __initUI(self):
        self.nodeGraphicsScene = NodeGraphicsScene(self)
        self.nodeGraphicsScene.setGraphicsScene(self.sceneWidth, self.sceneHeight)
        
    def addNode(self, node):
        self.nodes.append(node)
        
    def addEdge(self, edge):
        self.edges.append(edge)
        
    def removeNode(self, node):
        self.nodes.remove(node)
        
    def removeEdge(self, edge):
        self.edges.remove(edge)

class NodeGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene

        self.gridSize = 20
        self.gridSquare = 5
        self.sceenWidth, self.sceenHeight = 640000, 640000
        self.setSceneRect(self.sceenWidth//2, self.sceenHeight//2, self.sceenWidth, self.sceenHeight)

        self.penLight = QPen(WindowColor.DEFAULT_PEN_LIGHT)
        self.penLight.setWidth(1)
        self.penDark = QPen(WindowColor.DEFAULT_PEN_DARK)
        self.penDark.setWidth(2)
        self.setBackgroundBrush(WindowColor.DEFAULT_BACKGROUND)

    def setGraphicsScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)

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