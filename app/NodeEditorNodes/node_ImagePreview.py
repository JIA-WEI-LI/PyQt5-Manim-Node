from NodeEditor.Node.node_Node import Node

class Node_ImagePreview(Node):
    def __init__(self, scene, title="Image Preview", input=[1], output=[]):
        super().__init__(scene, title, input, output)