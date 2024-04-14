import math
import json

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QLine

from NodeEditor.Serialization.node_Serializable import Serializable
from common.color_sheet import color_manager

PENLIGHT_COLOR = color_manager.get_color("WindowColor", "BLENDER_PEN_LIGHT")
PENDARK_COLOR = color_manager.get_color("WindowColor", "BLENDER_PEN_DARK")
BACKGROUND_COLOR = color_manager.get_color("WindowColor", "BLENDER_BACKGROUND")

class Scene(Serializable):
    def __init__(self):
        super().__init__()
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

    def saveToFile(self, file_name):
        with open(file_name, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print(f"saving to {file_name} was successfull")

    def loadFromFile(self, file_name):
        with open(file_name, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

    def serialize(self):
        '''序列化資訊'''
        return {
            'id': self.id,
            'scene_width': self.sceneWidth,
            'scene_height': self.sceneHeight
        }
    
    def deserialize(self, data, hashmap={}):
        print(f"deserializating data ", data)
        raise NotImplemented()

class NodeGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene

        self.gridSize = 20
        self.gridSquare = 5
        self.sceenWidth, self.sceenHeight = 640000, 640000
        self.setSceneRect(self.sceenWidth//2, self.sceenHeight//2, self.sceenWidth, self.sceenHeight)

        self.penLight = QPen(PENLIGHT_COLOR)
        self.penLight.setWidth(1)
        self.penDark = QPen(PENDARK_COLOR)
        self.penDark.setWidth(2)
        self.setBackgroundBrush(BACKGROUND_COLOR)

    def setGraphicsScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        '''繪製視窗背景'''
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