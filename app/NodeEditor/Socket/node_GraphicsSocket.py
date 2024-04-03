from PyQt5.QtCore import QRectF 
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainter

from config.debug import DebugMode
from config.palette import SocketColor

class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1 ,parent=None) -> None:
        self.socket = socket
        super().__init__(socket.node.graphicsNode)

        self._radius = 5.0
        self._outline_width = 1.0
        self._pen = QPen(SocketColor.DEFAULT_OUTLINE)
        self._pen.setWidthF(self._outline_width)
        self.brush = QBrush(SocketColor.DEFAULT_COLOR_LIST[socket_type])

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self._pen)
        painter.drawEllipse(int(-self._radius), int(-self._radius), int(2*self._radius), int(2*self._radius))

    def boundingRect(self):
        '''提供一個矩形範圍，用於確定繪製物件的範圍'''
        return QRectF(
            -self._radius - self._outline_width,
            -self._radius - self._outline_width,
            2*(self._radius + self._outline_width),
            2*(self._radius + self._outline_width))