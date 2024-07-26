from PyQt5.QtGui import QColor

from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node
from common import *

class Node_Calculator(Node):
    def __init__(self, scene, op_code, title="Undefined Node", inputs=[1, 1], outputs=[1]):
        super().__init__(scene, title, inputs, outputs)
        self.op_code = op_code
        self.title = title

        self.node_type(0)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.content.addInputLabel("Input B", tooltip="Second input number")

class Node_Exhibit(Node):
    def __init__(self, scene, op_code, title="Exhibit Node", inputs=[1, 1], outputs=[1]):
        super().__init__(scene, title, inputs, outputs)
        self.op_code = op_code
        self.title = title

        self.node_type(1)
        self.content.addOutputLabel("Output")
        self.content.addInputLabel("Input A", tooltip="First input number")
        self.edit = self.content.addLineEdit("LineEdit")
        self.content.addPushButton(FluentIcon.PLAY, "Play")
        self.toggleButton = self.content.addToggleButton(FluentIcon.BACK_TO_WINDOW, "Window")

    def serialize(self):
        res = super().serialize()
        self.setSerializeValue(self.edit.text(), 2, 1)
        self.setSerializeValue(self.toggleButton.isChecked(), 4, 1, 'isChecked')
        return res