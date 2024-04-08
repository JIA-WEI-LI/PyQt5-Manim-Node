from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget, QStyleOptionGraphicsItem, QWidget
from PyQt5.QtGui import QPen, QFont, QBrush, QPainter, QPainterPath, QPolygonF

class NodeCuteline(QGraphicsItem):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.lines_points = []

        self._pen = QPen(Qt.GlobalColor.white)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 1, 1)
    
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.lines_points)
        painter.drawPolyline(poly)