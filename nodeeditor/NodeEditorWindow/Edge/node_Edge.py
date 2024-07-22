import gc
gc.enable()
from collections import OrderedDict

from .node_GraphicsEdge import NodeGraphicsEdgeDirect, NodeGraphicsEdgeBezier
from ..Serialization.node_Serializable import Serializable
from ..Socket.node_Socket import Socket
from common import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
DEBUG = DebugMode.NODE_EDGE

class Edge(Serializable):
    def __init__(self, scene, start_socket:Socket=None, end_socket:Socket=None, edge_type=EDGE_TYPE_DIRECT) -> None:
        super().__init__()
        self.scene = scene

        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        if DEBUG: print("Edge: ", self.nodeGraphicsEdge.posSource, "to", self.nodeGraphicsEdge.posDestination)
        # self.scene.nodeGraphicsScene.addItem(self.nodeGraphicsEdge)
        self.scene.addEdge(self)
        
    def __str__(self) -> str:
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    @property
    def start_socket(self): return self._start_socket
    @start_socket.setter
    def start_socket(self, value):
        # 如果之前有分配連結點，則刪除連結點
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)
        # 分配新的開始連結點
        self._start_socket = value
        if self.start_socket is not None:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self): return self._end_socket
    @end_socket.setter
    def end_socket(self, value):
        # 如果之前有分配連結點，則刪除連結點
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)
        # 分配新的結束連結點
        self._end_socket = value
        if self.end_socket is not None:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self): return self._edge_type
    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, 'nodeGraphicsEdge') and self.nodeGraphicsEdge is not None:
            self.scene.nodeGraphicsScene.removeItem(self.nodeGraphicsEdge)

        self._edge_type = value
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.nodeGraphicsEdge = NodeGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.nodeGraphicsEdge = NodeGraphicsEdgeBezier(self)
        else:
            self.nodeGraphicsEdge = NodeGraphicsEdgeBezier(self)

        self.scene.nodeGraphicsScene.addItem(self.nodeGraphicsEdge)

        if self.start_socket is not None:
            self.updatePositions()

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node.graphicsNode.pos().y()
        self.nodeGraphicsEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphicsNode.pos().x()
            end_pos[1] += self.end_socket.node.graphicsNode.pos().y()
            self.nodeGraphicsEdge.setDestination(*end_pos)
        else:
            self.nodeGraphicsEdge.setDestination(*source_pos)
        if DEBUG: print(" Start Socket: ", self.start_socket)
        if DEBUG: print(" End  Socket: ", self.end_socket)
        self.nodeGraphicsEdge.update()
        
    def remove_from_sockets(self):
        '''判斷移除連結點'''
        # FIXME：Fix in future 
        # if self.start_socket is not None:
        #     self.start_socket.removeEdge(None)
        # if self.end_socket is not None:
        #     self.end_socket.removeEdge(None)
        if DEBUG: print("::Edge  end_socket: ", self.end_socket, " start_socket: ", self.start_socket)
        self.end_socket = None
        self.start_socket = None
        if DEBUG: print("::Edge  end_socket: ", self.end_socket, " start_socket: ", self.start_socket)

    def remove(self):
        if DEBUG: print("# Removing Edge: ", self)
        if DEBUG: print(" - remove edge from all sockets")
        self.remove_from_sockets()
        if DEBUG: print(" - remove graphicsEdge")
        self.scene.nodeGraphicsScene.removeItem(self.nodeGraphicsEdge)
        self.nodeGraphicsEdge = None
        if DEBUG: print(" - remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass
        if DEBUG: print(" - everything is done.")

    def serialize(self):
        '''序列化資訊'''
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id if self.start_socket is not None else None),
            ('end', self.end_socket.id if self.end_socket is not None else None)
        ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type =  data['edge_type']
        return True