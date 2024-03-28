from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPen, QBrush, QPainter

from nodeEditor_Scene import Scene

class Edge:
    def __init__(self, scene:Scene, start_socket, end_socket) -> None:
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphicsEdge = NodeGraphicsEdgeDirect(self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)

class NodeGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge:Edge, parent=None):
        self.edge = edge

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawPath(self.path())

    def updatePath(self):
        '''當繪製新的線段時更新'''
        raise NotImplemented("This method has to be overriden in a child class")

class NodeGraphicsEdgeDirect(NodeGraphicsEdge):
    '''直線型連接線段'''
    def updatePath(self):
        pass

class NodeGraphicsEdgeBezier(NodeGraphicsEdge):
    '''貝茲曲線型連接線段'''
    def updatePath(self):
        pass