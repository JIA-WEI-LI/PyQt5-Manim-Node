from PyQt5.QtGui import QColor

from CalculatorWindow.calculator_config import *
from CalculatorWindow.calculator_node_base import *
from common import *

@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_INPUT, "Input", inputs=[], outputs=[3])

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_OUTPUT, "Output", inputs=[1], outputs=[])
        self.node_color = FluentColor.GOLD.color()

@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_ADD, "Add")

@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_SUB, "Substract")

@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_MUL, "Multiply")

@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_DIV, "Divide")