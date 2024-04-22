from collections import OrderedDict

from ..Serialization.node_Serializable import Serializable
from .node_GraphicsSocket import NodeGraphicsSocket
from config.debug import DebugMode

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node, *,  position, index:int=0, socket_type=1, space:int=0) -> None:
        super().__init__()
        self.node = node
        self.position = position
        self.index = index
        
        self.socket_type = socket_type
        
        if DebugMode.NODE_SOCKET: print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.graphicsSocket = NodeGraphicsSocket(self, self.socket_type)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position, space = space))
        
        self.edge = None
 
    def __str__(self) -> str:
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def getSocketPosition(self, *, space:int=0):
        if DebugMode.NODE_SOCKET: print("  Get Socket Pos: ", self.index, self.position, " node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position, space=space)
        if DebugMode.NODE_SOCKET: print("  res: ", res)
        return res
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
    
    def serialize(self):
        '''序列化資訊'''
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('position', self.position),
            ('socket_type', self.socket_type)
        ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        hashmap[data['id']] = self
        return True