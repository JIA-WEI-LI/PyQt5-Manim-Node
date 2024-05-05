import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .Edge.node_Edge import Edge
from .Node.node_Node import Node
from .nodeEditor_Scene import Scene
from .nodeEditor_GraphicsView import NodeGraphicsView

from config.debug import DebugMode, DebugTimer
from NodeEditorNodes.node_Calculator import *
from NodeEditorNodes.Testing_node import Node_Test

class NodeEditorWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.filename = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 創建圖像場景
        self.scene = Scene()
        self.addNodes()

        # 創建圖像視圖
        self.view = NodeGraphicsView(self.scene.nodeGraphicsScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.has_been_modified

    def isFilanameSet(self):
        return self.filename is not None
    
    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilanameSet() else "New Graph"
        # TODO: 新增 has_been_modified 邏輯
        return name 

    def addNodes(self):
        '''新增節點'''
        # 放置初始節點
        node_int0 = Node_Integer(self.scene)
        node_int1 = Node_Integer(self.scene)
        node1 = Node_Add(self.scene)
        node2 = Node_Substract(self.scene)
        node3 = Node_Multiply(self.scene)
        node4 = Node_Divide(self.scene)
        node_Test = Node_Test(self.scene)
        node_int0.setPos(-100, -100)
        node_int1.setPos(-200, -200)
        node1.setPos(0, 0)
        node2.setPos(100, 100)
        node3.setPos(200, 200)
        node4.setPos(300, 300)
        node_Test.setPos(600, 0)

        # edge1 = Edge(self.scene, node2.outputs[0], node1.inputs[0])
        # edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)