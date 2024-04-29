import gc
gc.enable()
from collections import OrderedDict

from ..Serialization.node_Serializable import Serializable
from .node_GraphicsSocket import NodeGraphicsSocket
from config.debug import DebugMode

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node, *, index:int=0, position=LEFT_BOTTOM, socket_type=1, space:int=0, muliti_edges:bool=True) -> None:
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.is_multi_edges = muliti_edges
        
        if DebugMode.NODE_SOCKET: print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.graphicsSocket = NodeGraphicsSocket(self, self.socket_type)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position, space = space))
        
        self.edges = []
 
    def __str__(self) -> str:
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def getSocketPosition(self, *, space:int=0):
        # if DebugMode.NODE_SOCKET: print("  Get Socket Pos: ", self.index, self.position, " node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position, space=space)
        # if DebugMode.NODE_SOCKET: print("  res: ", res)
        return res
        
    def addEdge(self, edge):
        self.edges.append(edge)

    def removeEdge(self, edge):
        # BUG：切割線段或點擊時有機率無錯誤輸出閃退(常見於移動節點後)
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W: ", "Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not a list!")

    def removeAllEdges(self):
        # BUG：切割線段或點擊時有機率無錯誤輸出閃退(常見於移動節點後)
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()
    
    def serialize(self):
        '''序列化資訊'''
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type)
        ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self
        return True