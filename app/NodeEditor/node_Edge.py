from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainter, QPainterPath, QPen

from .node_Socket import Socket
from .nodeEditor_Scene import Scene

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
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.nodeGraphicsScene.removeItem(self.nodeGraphicsEdge)
        self.nodeGraphicsEdge = None
        self.scene.removeEdge(self)

class NodeGraphicsEdge(QGraphicsPathItem):
    '''繪製基礎連接線段'''
    def __init__(self, edge:Edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        self._pen = QPen(EdgeColor.ORANGE)
        self._pen.setWidthF(2.0)
        self._penSelected = QPen(EdgeColor.DEFAULT_PEN_SELECTED)
        self._penSelected.setWidthF(2.0)
        self._penDragging = QPen(EdgeColor.ORANGE)
        self._penDragging.setStyle(Qt.PenStyle.DashLine)

        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]
        
    def setSource(self, x, y):
        self.posSource = [x, y]
    
    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        
        if self.edge.end_socket is None:
            painter.setPen(self._penDragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._penSelected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        '''當繪製新的線段時更新'''
        raise NotImplemented("This method has to be overriden in a child class")

class NodeGraphicsEdgeDirect(NodeGraphicsEdge):
    '''直線型連接線段'''
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class NodeGraphicsEdgeBezier(NodeGraphicsEdge):
    '''貝茲曲線型連接線段'''
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0]-s[0]) * 0.5
        if s[0] > d[0]: dist *= -1
        
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1], self.posDestination[0], self.posDestination[1])
        self.setPath(path)