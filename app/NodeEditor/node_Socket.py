from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainter

from config.debug import DEBUG_MODE
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
        
        if DEBUG_MODE: print("Socket -- creating with", self.index, self.position, "for node", self.node)

        self.graphicsSocket = NodeGraphicsSocket(self.socket_type, parent=self.node.graphicsNode)
        self.graphicsSocket.setPos(*self.node.getSocketPosition(index, position))
        
        self.edge = None
        
    def getSocketPosition(self):
        if DEBUG_MODE: print("  Get Socket Pos: ", self.index, self.position, " node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position)
        if DEBUG_MODE: print("  res: ", res)
        return res
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None

class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, socket_type=1 ,parent=None) -> None:
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 1.0
        self._pen = QPen(SocketColor.DEFAULT_OUTLINE)
        self._pen.setWidthF(self.outline_width)
        self.brush = QBrush(SocketColor.DEFAULT_COLOR_LIST[socket_type])

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self._pen)
        painter.drawEllipse(int(-self.radius), int(-self.radius), int(2*self.radius), int(2*self.radius))

    def boundingRect(self):
        '''提供一個矩形範圍，用於確定繪製物件的範圍'''
        return QRectF(
            -self.radius - self.outline_width,
            -self.radius - self.outline_width,
            2*(self.radius + self.outline_width),
            2*(self.radius + self.outline_width))