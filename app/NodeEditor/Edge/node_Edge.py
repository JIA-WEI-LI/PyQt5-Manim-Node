from collections import OrderedDict

from .node_GraphicsEdge import NodeGraphicsEdgeDirect, NodeGraphicsEdgeBezier
from ..Serialization.node_Serializable import Serializable
from ..Socket.node_Socket import Socket

from config.debug import DebugMode

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
DEBUG = DebugMode.NODE_EDGE

class Edge(Serializable):
    def __init__(self, scene, start_socket:Socket, end_socket:Socket, edge_type=EDGE_TYPE_DIRECT) -> None:
        super().__init__()
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.nodeGraphicsEdge = NodeGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else NodeGraphicsEdgeBezier(self)

        self.updatePositions()
        if DEBUG: print("Edge: ", self.nodeGraphicsEdge.posSource, "to", self.nodeGraphicsEdge.posDestination)
        self.scene.nodeGraphicsScene.addItem(self.nodeGraphicsEdge)
        self.scene.addEdge(self)
        
    def __str__(self) -> str:
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

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
        # 經過修正後
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

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
            ('start', self.start_socket.id),
            ('end', self.end_socket.id)
        ])
    
    def deserialize(self, data, hashmap={}):
        raise False