from PyQt5.QtGui import QColor

from CalculatorWindow.calculator_config import *
from CalculatorWindow.calculator_node_base import *
from common import *

@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_INPUT, "Input", inputs=[], outputs=[3])
        self.content.addOutputLabel("Iutput")

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_OUTPUT, "Output", inputs=[1], outputs=[])
        self.node_color = FluentColor.GOLD.color()
        self.content.addInputLabel("Output")

@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_ADD, "Add")
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_SUB, "Substract")
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_MUL, "Multiply")
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_DIV, "Divide")
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")