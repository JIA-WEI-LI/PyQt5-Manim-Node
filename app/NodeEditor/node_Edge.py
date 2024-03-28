from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainter, QPainterPath, QPen

from .node_Socket import Socket
from .nodeEditor_Scene import Scene

from config.palette import EdgeColor

class Edge:
    def __init__(self, scene:Scene, start_socket:Socket, end_socket:Socket) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.nodeGraphicsEdge = NodeGraphicsEdgeDirect(self)

        self.scene.nodeGraphicsScene.addItem(self.nodeGraphicsEdge)

class NodeGraphicsEdge(QGraphicsPathItem):
    '''繪製基礎連接線段'''
    def __init__(self, edge:Edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        self._pen = QPen(EdgeColor.DEFAULT_PEN)
        self._pen.setWidthF(2.0)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)
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
    def __init__(self, edge: Edge, parent=None):
        super().__init__(edge, parent)
        
    def updatePath(self):
        pass