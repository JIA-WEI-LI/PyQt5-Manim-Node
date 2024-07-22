from typing import Union
from PyQt5.QtCore import QRectF 
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPainter, QColor

from common import *

socket_color_list = {
    0: BlenderColor.TEAL_GREEN.color(),
    1: BlenderColor.TEAL_GREEN.color(),
    2: BlenderColor.TEAL_GREEN.color(),
    3: BlenderColor.PALE_AQUA.color(),
    4: BlenderColor.TEAL_GREEN.color(),
    'default': BlenderColor.DARK_CHARCOAL.color()
}

class NodeGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type:int=0 ,parent=None) -> None:
        self.socket = socket
        super().__init__(socket.node.graphicsNode)

        self._radius = 7.0
        self._outline_width = 1.0
        self._pen = QPen(QColor("black"))
        self._pen.setWidthF(self._outline_width)
        self.brush = QBrush(self.getSocketColor(socket_type))

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
    
    def getSocketColor(self, socket_color: Union[str, FluentColor, BlenderColor] = 'default'):
        # TODO: 開放可以使用已定義顏色
        if hasattr(socket_color, FluentColor) or hasattr(socket_color, BlenderColor):
            return socket_color
        else:
            return socket_color_list.get(socket_color, socket_color_list['default'])