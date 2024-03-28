from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainter

from config.palette import SocketColor

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket:
    def __init__(self, node, index:int=0, position=LEFT_TOP) -> None:
        self.node = node
        self.graphicsSocket = NodeGraphicsSocket()
        self.position = position

class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem=None) -> None:
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 1.0
        self.pen = QPen(SocketColor.DEFAULT_OUTLINE)
        self.pen.setWidthF(self.outline_width)
        self.brush = QBrush(SocketColor.DEFAULT_BACKGROUND)

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)