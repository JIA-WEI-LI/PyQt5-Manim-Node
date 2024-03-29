from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainter, QPainterPath, QPen

from .node_Socket import Socket
from .nodeEditor_Scene import Scene

from config.palette import EdgeColor

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge:
    def __init__(self, scene:Scene, start_socket:Socket, end_socket:Socket, type=EDGE_TYPE_DIRECT) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.nodeGraphicsEdge = NodeGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else NodeGraphicsEdgeBezier(self)

        self.updatePositions()
        print("Edge: ", self.nodeGraphicsEdge.posSource, " to: ", self.nodeGraphicsEdge.posDestination)
        self.scene.nodeGraphicsScene.addItem(self.nodeGraphicsEdge)
        
    def updatePositions(self):
        self.nodeGraphicsEdge.setSource(*self.start_socket.getSocketPosition())
        if self.end_socket is not None:
            self.nodeGraphicsEdge.setDestination(*self.end_socket.getSocketPosition())
        self.nodeGraphicsEdge.update()
        
    def remove_from_sockets(self):
        '''判斷移除連結點'''
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket.edge = None
        self.start_socket.edge = None
        
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

        self._pen = QPen(EdgeColor.DEFAULT_PEN)
        self._pen.setWidthF(2.0)
        self._penSelected = QPen(EdgeColor.DEFAULT_PEN_SELECTED)
        self._penSelected.setWidthF(2.0)

        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]
        
    def setSource(self, x, y):
        self.setSource = [x, y]
    
    def setDestination(self, x, y):
        self.setDestination = [x, y]

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen if not self.isSelected() else self._penSelected)
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