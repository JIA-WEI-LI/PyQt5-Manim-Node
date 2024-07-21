from PyQt5.QtGui import QColor

from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node

class Node_Calculator(Node):
    def __init__(self, scene, op_code, title="Undefined Node", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.op_code = op_code
        self.title = title

        self.node_type(0)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")