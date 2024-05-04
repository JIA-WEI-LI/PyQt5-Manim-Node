import math
import json
from collections import OrderedDict

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QLine

from .Edge.node_Edge import Edge
from .Node.node_Node import Node
from .Serialization.node_Serializable import Serializable
from .Scene.nodeEditor_SceneHistory import SceneHistory
from .Scene.nodeEditor_SceneClipboard import SceneClipboard
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
        
        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

    @property
    def has_been_modified(self):
        return False
        return self._has_been_modified
    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)
        
    def initUI(self):
        self.nodeGraphicsScene = NodeGraphicsScene(self)
        self.nodeGraphicsScene.setGraphicsScene(self.sceneWidth, self.sceneHeight)
        
    def addNode(self, node):
        self.nodes.append(node)
        
    def addEdge(self, edge):
        self.edges.append(edge)
        
    def removeNode(self, node):
        if node in self.nodes: self.nodes.remove(node)
        else: print("!W: ", "Scene::removeNode", "wanna remove edge", node, "from self.nodes but it's not a list!")
        
    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W: ", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not a list!")

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def saveToFile(self, file_name):
        with open(file_name, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            print(f"Saving to {file_name} was successfull")

            self.has_been_modified = False

    def loadFromFile(self, file_name):
        with open(file_name, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            print(f"Loading {file_name} was successfull")

            self.has_been_modified = False

    def serialize(self):
        '''序列化資訊'''
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.sceneWidth),
            ('scene_height', self.sceneHeight),
            ('nodes', nodes),
            ('edges', edges)
            ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}

        if restore_id: self.id = data['id']

        # 創造節點
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap, restore_id)
        
        # 創造線段
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True

class NodeGraphicsScene(QGraphicsScene):
    '''繪製節點編輯器視窗背景'''
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