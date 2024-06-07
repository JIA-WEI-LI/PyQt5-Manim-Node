from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QLabel

from NodeEditorWindow.Node.node_Node import Node
from NodeEditorWindow.Node.node_ContentWidget import NodeContentWidget
from NodeEditorWindow.Node.node_GraphicsNode import NodeGraphicsNode
from NodeEditorWindow.Socket.node_Socket import LEFT_BOTTOM, RIGHT_TOP
from common.utils import dumpException

class CalcNode(Node):
    def __init__(self, scene, op_code, op_title, inputs=[2, 2], outputs=[1]):
        self.op_code = op_code
        self.op_title = op_title

        super().__init__(scene, self.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.graphicsNode = NodeGraphicsNode(self)

class CalcContent(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)
        # self.addInputLabel()
        # print("node: ", self.node)
        # print("node.graphicsNode: ", self.node.graphicsNode)