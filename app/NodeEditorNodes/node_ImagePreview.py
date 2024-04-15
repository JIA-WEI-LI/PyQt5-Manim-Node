from components import *
from NodeEditor.Node.node_Node import Node
from NodeEditor.Socket.node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM

class Node_ImagePreview(Node):
    def __init__(self, scene, title="Image Preview", input=[]):
        super().__init__(scene, title, input)
        self.graphicsNode.height = self.graphicsNode.titleHeight + 2 * self.graphicsNode.padding + 5 * self.graphicsNode.node.socketSpace
        self.content.addGraphicsView('app\\resources\\screenshot\\20240329_meme.png')

        socket = Socket(node=self, index=1, position=LEFT_BOTTOM, socket_type=1, space=3)
        self.inputs.append(socket)
        self.content.addLabel(f"Image")
        