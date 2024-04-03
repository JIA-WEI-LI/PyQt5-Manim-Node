from .node_GraphicsSocket import NodeGraphicsSocket
from config.debug import DebugMode
from config.palette import SocketColor

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket:
    def __init__(self, node, index:int=0, position=LEFT_TOP, socket_type=1) -> None:
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        
        if DebugMode.NODE_SOCKET: print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.graphicsSocket = NodeGraphicsSocket(self, self.socket_type)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position))
        
        self.edge = None
 
    def __str__(self) -> str:
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def getSocketPosition(self):
        if DebugMode.NODE_SOCKET: print("  Get Socket Pos: ", self.index, self.position, " node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position)
        if DebugMode.NODE_SOCKET: print("  res: ", res)
        return res
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None