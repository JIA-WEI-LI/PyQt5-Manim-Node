from PyQt5.QtCore import QRectF 
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainter, QColor

from common.color_sheet import color_manager
from config.debug import DebugMode

PEN_COLOR = color_manager.get_color("SocketColor", "DEFAULT_OUTLINE")
BRUSH_COLORLIST = color_manager.get_color_list("SocketColor", "DEFAULT_COLOR_LIST")

class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1 ,parent=None) -> None:
        self.socket = socket
        super().__init__(socket.node.graphicsNode)

        self._radius = 7.0
        self._outline_width = 1.0
        # self._pen = QPen(SocketColor.DEFAULT_OUTLINE)
        self._pen = QPen(PEN_COLOR)
        self._pen.setWidthF(self._outline_width)
        # self.brush = QBrush(SocketColor.DEFAULT_COLOR_LIST[socket_type])
        self.brush = QBrush(QColor(BRUSH_COLORLIST[socket_type]))

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