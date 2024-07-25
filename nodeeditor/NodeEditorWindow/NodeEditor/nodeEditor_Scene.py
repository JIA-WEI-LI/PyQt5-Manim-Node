import os
import math
import json
from collections import OrderedDict

from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QLine, pyqtSignal

from ..Edge.node_Edge import Edge
from ..Node.node_Node import Node
from ..Serialization.node_Serializable import Serializable
from ..Scene.nodeEditor_SceneHistory import SceneHistory
from ..Scene.nodeEditor_SceneClipboard import SceneClipboard
from common import *

class InvalidFile(Exception): pass

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.sceneWidth, self.sceneHeight = 64000, 64000
        
        self._has_been_modified = False
        self._last_selected_items = []
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.nodeGraphicsScene.itemSelected.connect(self.onItemSelected)
        self.nodeGraphicsScene.itemsDeselected.connect(self.onItemsDeselected)

    def initUI(self):
        self.nodeGraphicsScene = NodeGraphicsScene(self)
        self.nodeGraphicsScene.setGraphicsScene(self.sceneWidth, self.sceneHeight)

    def onItemSelected(self):
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            self.history.storeHistory("Selected Changed")
            for callback in self._item_selected_listeners: callback()

    def onItemsDeselected(self):
        self.resetLastSelectedStates()
        if self._last_selected_items != []:
            self._last_selected_items = []
            self.history.storeHistory("Deselected Everything")
            for callback in self._items_deselected_listeners: callback()

    def isModified(self):
        return self.has_been_modified
    
    def getSelectedItems(self):
        return self.nodeGraphicsScene.selectedItems()

    @property
    def has_been_modified(self):
        # return False
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

    def addItemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback)

    def addItemsDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    def addDragEnterlisteners(self, callback):
        self.nodeGraphicsScene.views()[0].addDragEnterListener(callback)

    def addDropListeners(self, callback):
        self.nodeGraphicsScene.views()[0].addDropEnterListener(callback)

    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.graphicsNode._last_selected_state = False
        for edge in self.edges:
            edge.nodeGraphicsEdge._last_selected_state = False
        
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

    def loadFromFile(self, filename):
        with open(filename, "r", encoding='utf-8') as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data)
                self.deserialize(data)
                self.has_been_modified = False
                print(f"Loading {filename} was successfull")
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

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
    itemSelected = pyqtSignal()
    itemsDeselected = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene

        self.gridSize = 20
        self.gridSquare = 5
        self.sceenWidth, self.sceenHeight = 640000, 640000
        self.setSceneRect(self.sceenWidth//2, self.sceenHeight//2, self.sceenWidth, self.sceenHeight)

        self.penLight = QPen(BlenderColor.DARK_SLATE.color())
        self.penLight.setWidth(1)
        self.penDark = QPen(BlenderColor.DARK_IRON_GRAY.color())
        self.penDark.setWidth(2)
        self.setBackgroundBrush(BlenderColor.DARK_CHARCOAL.color())

    def dragMoveEvent(self, event):
        pass

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