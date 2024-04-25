from BlenderStyleWidget import *
from NodeEditor.Node.node_Node import Node

class Node_Test(Node):
    def __init__(self, scene, title="Node_Test", input=[1, 2, 3], output=[1, 2, 3, 1]):
        super().__init__(scene, title, input, output)

        self.content.addLabel("Output", isOutput=True)
        self.content.addLineEdit("Line Edit", tooltip="New Tooltip")
        self.content.addProgressBar(tooltip="測試文件")
        self.content.addComboBox(["List 1", "List 1", "List 1"])
        self.content.addLabel("Test Label 1")
        self.content.addLabel("Test Label 2")
        self.content.addLabel("Test Label 3")

    def get_height(self):
        return self.content.vboxLayout.geometry().height()