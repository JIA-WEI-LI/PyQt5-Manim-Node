from PyQt5.QtGui import QColor

from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node
from common.color_sheet import color_manager

class Node_Calculator(Node):
    def __init__(self, scene, op_code, title="Undefined Node", input=[1, 1], output=[1]):
        super().__init__(scene, title, input, output)
        self.op_code = op_code
        self.title = title

        self.node_type(0)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Normalize(Node):
    def __init__(self, scene, title="Normalize", input=[], output=[1]):
        super().__init__(scene, title, input, output)
        
        self.node_type(3)
        self.content.addOutputLabel("Value")
        self.content.addProgressBar("Value", minimum=0, maximum=1, tooltip="Output between 0 and 1")

class Node_Integer(Node):
    def __init__(self, scene, title="Integer", input=[], output=[1]):
        super().__init__(scene, title, input, output)
        
        self.node_type(3)
        self.content.addOutputLabel("Value")
        self.content.addSpinBox("Integer", minimum=0, maximum=100000, tooltip="Output Integer")

class Node_String(Node):
    def __init__(self, scene, title="String", input=[], output=[2]):
        super().__init__(scene, title, input, output)
        
        self.node_type(3)
        self.content.addOutputLabel("String")
        self.content.addLineEdit("")

class Node_Boolean(Node):
    def __init__(self, scene, title="Boolean", input=[], output=[4]):
        super().__init__(scene, title, input, output)
        
        self.node_type(3)
        self.content.addOutputLabel("boolean")
        self.content.addCheckbox("boolean")

class Node_ValueToString(Node):
    def __init__(self, scene, title="Value to String", input=[1], output=[2]):
        super().__init__(scene, title, input, output)

        self.node_type(1)
        self.content.addOutputLabel("String")
        self.content.addSpinBox("Value", minimum=0, maximum=100000, tooltip="Intput Integer")

class Node_StringToValue(Node):
    def __init__(self, scene, title="String to Value", input=[2], output=[0, 1]):
        super().__init__(scene, title, input, output)

        self.node_type(1)
        self.content.addComboBox(["Interger", "Float", "Double"])
        self.content.addOutputLabel("Value")
        self.content.addLineEdit("String")

class Node_Color(Node):
    def __init__(self, scene, title="Color", input=[], output=[0, 3]):
        super().__init__(scene, title, input, output)
        
        self.node_type(3)
        self.content.addComboBox(["RGB", "HSV", "HEX"])
        self.content.addOutputLabel("RGB")
        self.content.addColorPickerButton()