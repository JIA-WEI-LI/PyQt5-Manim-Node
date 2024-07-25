from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget
from PyQt5.QtGui import QPen, QPainter, QPolygonF, QPainterPath

DEBUG = True

class NodeCuteline(QGraphicsItem):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.lines_points = []

        self._pen = QPen(Qt.GlobalColor.white)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        # return QRectF(0, 0, 1, 1)
        return self.shape().boundingRect()

    def shape(self):
        poly = QPolygonF(self.lines_points)

        if len(self.lines_points) > 1:
            path = QPainterPath(self.lines_points[0])
            for pt in self.lines_points[1:]:
                path.lineTo(pt)
        else:
            path = QPainterPath(QPointF(0, 0))
            path.lineTo(QPointF(1, 1))

        return path
    
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.lines_points)
        painter.drawPolyline(poly)