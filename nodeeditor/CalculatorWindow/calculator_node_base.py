from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QLabel

from NodeEditorWindow.Node.node_Node import Node
from NodeEditorWindow.Socket.node_Socket import LEFT_BOTTOM, RIGHT_TOP
from common.utils import dumpException

class CalcNode(Node):
    def __init__(self, scene, op_code, op_title, inputs=[2,2], outputs=[1]):
        self.op_code = op_code
        self.op_title = op_title

        super().__init__(scene, self.op_title, inputs, outputs)