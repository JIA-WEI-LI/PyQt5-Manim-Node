from PyQt5.QtGui import QColor

from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node
from common.color_sheet import color_manager

class Node_Add(Node):
    def __init__(self, scene, title="Add", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0]
        
        self.content.addOutputLabel("Output")
        label1 = self.content.addInputLabel("Input A", tooltip="First input number")
        label2 = self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Substract(Node):
    def __init__(self, scene, title="Substract", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0]
        
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Multiply(Node):
    def __init__(self, scene, title="Multiply", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0]
        
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Divide(Node):
    def __init__(self, scene, title="Divide", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[0]
        
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Normalize(Node):
    def __init__(self, scene, title="Normalize", input=[], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[3]
        
        self.content.addOutputLabel("Value")
        self.content.addProgressBar("Value", minimum=0, maximum=1, tooltip="Output between 0 and 1")

class Node_Integer(Node):
    def __init__(self, scene, title="Integer", input=[], output=[1]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[3]
        
        self.content.addOutputLabel("Value")
        self.content.addSpinBox("Integer", minimum=0, maximum=100000, tooltip="Output Integer")

class Node_String(Node):
    def __init__(self, scene, title="String", input=[], output=[2]):
        super().__init__(scene, title, input, output)
        self.node_color = color_manager.get_color_list("NodeColor", "BLENDER_TITLE_LIST")[3]
        
        self.content.addOutputLabel("String")
        self.content.addLineEdit("")

class Node_ValueToString(Node):
    def __init__(self, scene, title="Value to String", input=[1], output=[2]):
        super().__init__(scene, title, input, output)

        self.content.addOutputLabel("String")
        self.content.addSpinBox("Value", minimum=0, maximum=100000, tooltip="Intput Integer")

class Node_StringToValue(Node):
    def __init__(self, scene, title="String to Value", input=[2], output=[0, 1]):
        super().__init__(scene, title, input, output)

        self.content.addComboBox(["Interger", "Float", "Double"])
        self.content.addOutputLabel("Value")
        self.content.addLineEdit("String")

class Node_Vector2(Node):
    def __init__(self, scene, title="Vector 2", input=[1, 1], output=[3]):
        super().__init__(scene, title, input, output)

        self.content.addOutputLabel("Vector")
        self.content.addVectorSpinBox(degree=["x", "y"])

class Node_Vector3(Node):
    def __init__(self, scene, title="Vector 3", input=[1, 1, 1], output=[3]):
        super().__init__(scene, title, input, output)

        self.content.addOutputLabel("Vector")
        self.content.addVectorSpinBox()