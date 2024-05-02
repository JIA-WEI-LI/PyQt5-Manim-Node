from NodeEditorWindow.BlenderStyleWidget import *
from NodeEditorWindow.Node.node_Node import Node

class Node_Add(Node):
    def __init__(self, scene, title="Number Add", input=[1, 1, 2]):
        super().__init__(scene, title, input)
        
        self.content.addPushButton("Push Button", tooltip="New Pushbutton Tooltip")
        self.content.addProgressBar("New Value", tooltip="New ProgressBar Tooltip")
        self.content.addCheckbox("TEST", tooltip="New Checkbox Tooltip")