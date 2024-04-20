from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .Edge.node_Edge import Edge
from .Node.node_Node import Node
from .nodeEditor_Scene import Scene
from .nodeEditor_GraphicsView import NodeGraphicsView

from config.debug import DebugMode, DebugTimer
from config.icon import Icon
from NodeEditorNodes.node_Add import Node_Add, Node_Test

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
        self.scene = Scene()
        self.addNodes()

        # 創建圖像視圖
        self.view = NodeGraphicsView(self.scene.nodeGraphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

    def addNodes(self):
        '''新增節點'''
        # 放置初始節點
        node1 = Node_Add(self.scene)
        node2 = Node_Test(self.scene)
        node1.setPos(-350, -250)
        node2.setPos(0, 0)

        # edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        # edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)