from BlenderStyleWidget import *
from NodeEditor.Node.node_Node import Node

class Node_Test(Node):
    def __init__(self, scene, title="Node_Test", input=[1, 1, 1], output=[2, 2, 2]):
        super().__init__(scene, title, input, output)

        self.content.addLabel("Output 1", isOutput=True)
        self.content.addLabel("Output 2", isOutput=True)
        self.content.addLabel("Output 3", isOutput=True)
        self.content.addLabel("Input 1")
        self.content.addLabel("Input 2")
        self.content.addLabel("Input 3")