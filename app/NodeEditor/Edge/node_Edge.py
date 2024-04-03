from .node_GraphicsEdge import NodeGraphicsEdgeDirect, NodeGraphicsEdgeBezier
from ..Socket.node_Socket import Socket
from ..nodeEditor_Scene import Scene

from config.debug import DebugMode
from config.palette import EdgeColor

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge:
    def __init__(self, scene:Scene, start_socket:Socket, end_socket:Socket, edge_type=EDGE_TYPE_DIRECT) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.nodeGraphicsEdge = NodeGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else NodeGraphicsEdgeBezier(self)

        self.updatePositions()
        if DebugMode.NODE_EDGE: print("Edge: ", self.nodeGraphicsEdge.posSource, "to", self.nodeGraphicsEdge.posDestination)
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
        if DebugMode.NODE_EDGE: print(" Start Socket: ", self.start_socket)
        if DebugMode.NODE_EDGE: print(" End  Socket: ", self.end_socket)
        self.nodeGraphicsEdge.update()
        
    def remove_from_sockets(self):
        '''判斷移除連結點'''
        # 經過修正後
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.nodeGraphicsScene.removeItem(self.nodeGraphicsEdge)
        self.nodeGraphicsEdge = None
        self.scene.removeEdge(self)