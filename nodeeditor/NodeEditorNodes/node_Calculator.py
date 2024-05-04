from PyQt5.QtGui import QColor

from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node
from common.color_sheet import color_manager

class Node_Add(Node):
    def __init__(self, scene, title="Add", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = QColor(color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0])
        
        self.content.addLabel("Output", isOutput=True)
        self.content.addLabel("Input A", tooltip="First input number")
        self.content.addLabel("Input B", tooltip="Second input number")

class Node_Substract(Node):
    def __init__(self, scene, title="Substract", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = QColor(color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0])
        
        self.content.addLabel("Output", isOutput=True)
        self.content.addLabel("Input A", tooltip="First input number")
        self.content.addLabel("Input B", tooltip="Second input number")

class Node_Multiply(Node):
    def __init__(self, scene, title="Multiply", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = QColor(color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0])
        
        self.content.addLabel("Output", isOutput=True)
        self.content.addLabel("Input A", tooltip="First input number")
        self.content.addLabel("Input B", tooltip="Second input number")

class Node_Divide(Node):
    def __init__(self, scene, title="Divide", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = QColor(color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0])
        
        self.content.addLabel("Output", isOutput=True)
        self.content.addLabel("Input A", tooltip="First input number")
        self.content.addLabel("Input B", tooltip="Second input number")

class Node_Integer(Node):
    def __init__(self, scene, title="Integer", input=[], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = QColor(color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[3])
        
        self.content.addProgressBar("Integer", minimum=0, maximum=100, tooltip="Output Integer")