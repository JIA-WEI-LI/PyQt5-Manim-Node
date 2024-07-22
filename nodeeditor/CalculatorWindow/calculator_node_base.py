from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QLabel

from NodeEditorWindow.Node.node_Node import Node
from NodeEditorWindow.Node.node_ContentWidget import NodeContentWidget
from NodeEditorWindow.Node.node_GraphicsNode import NodeGraphicsNode
from NodeEditorWindow.Socket.node_Socket import LEFT_BOTTOM, RIGHT_TOP
from common.utils import dumpException

class CalcGraphicsNode(NodeGraphicsNode):
    def initSize(self):
        super().initSize()
        self.width = 180  # 節點寬高
        self._padding = 4.0  # 連結點位置出血區
        self.edgeSize = 10.0
        self.titleHeight = 26.0
        self.titlePadding = 6.0

class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    def __init__(self, scene, inputs=[2, 2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.graphicsNode = NodeGraphicsNode(self)

    def initSetting(self):
        super().initSetting()
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res: ", res)

class CalcContent(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)