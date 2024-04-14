from NodeEditor.Node.node_Node import Node
from NodeEditor.Edge.node_Edge import Edge
from NodeEditor.Socket.node_Socket import Socket

class Serializable():
    def __init__(self) -> None:
        self.id = id(self)

    def serialize(self):
        raise NotImplemented()
    
    def deserialize(self, data, hashmap={}):
        raise NotImplemented()