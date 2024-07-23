from PyQt5.QtGui import QColor

from CalculatorWindow.calculator_config import *
from CalculatorWindow.calculator_node_base import *
from common import *

@register_node(OP_NODE_OTHER)
class CalcNode_Div(CalcNode):
    icon = Icon(FluentIcon.ALIGNMENT)
    op_code = OP_NODE_OTHER
    op_title = "Other"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[3, 3], outputs=[3])
        self.content.addOutputLabel("Output")
        self.content.addPushButton(FluentIcon.BACK_TO_WINDOW, "Back to window")
        self.content.addToggleButton(text="Back to window")

@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.content.addOutputLabel("String")
        self.edit = self.content.addLineEdit("Input")

    def serialize(self):
        res = super().serialize()
        self.setSerializeValue(self.edit.text(), 1, 1)
        return res

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[0])
        self.edit = self.content.addLineEdit("Input")
        self.edit.setReadOnly(True)
        self.content.addInputLabel("Output")

    def serialize(self):
        res = super().serialize()
        self.setSerializeValue(self.edit.text(), 0, 1)
        return res


@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_SUB
    op_title = "Sub"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_MUL
    op_title = "Mul"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = Icon(FluentIcon.ADD)
    op_code = OP_NODE_DIV
    op_title = "Div"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")