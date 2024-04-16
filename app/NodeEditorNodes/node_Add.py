from components import *
from NodeEditor.Node.node_Node import Node

class Node_Add(Node):
    def __init__(self, scene, title="Number Add", input=[1, 1]):
        super().__init__(scene, title, input)
        
        self.content.addProgressBar()
        self.content.addProgressBar("New Value", tooltip="New ProgressBar Tooltip")