from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.QtGui import QPen, QFont, QBrush, QPainter, QPainterPath

from config.debug import DebugMode
from config.palette import NodeColor

class NodeGraphicsNode(QGraphicsItem):
    def __init__(self, node ,parent=None):
        super().__init__(parent=parent)
        self.node = node
        self.content = self.node.content
        
        self.titleFont = QFont("Ubuntu", 10)
        
        self.width = 180  # 節點寬高
        # self.height = 240
        self.padding = 4.0  # 連結點位置出血區
        self.edgeSize = 10.0
        self.titleHeight = 24.0
        self.titlePadding = 6.0

        # 節點高度隨輸入與輸出點多寡改變
        self.height = self.titleHeight + 2 * self.padding + 0* self.edgeSize + (len(self.node.input) + len(self.node.output)) * self.node.socketSpace
        
        # 標題
        self.initTitle()
        self.title = self.node.title
        
        # 連結點
        self.initSockets()

        # 內部元素
        self.initContent()
        
        self.initUI()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        self.node.updateConnectedEdges()
        
    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.titleItem.setPlainText(self._title)
        
    def boundingRect(self):
        '''邊界'''
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()
        
    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    
    def initTitle(self):
        '''節點主名稱標題'''
        self.titleItem = QGraphicsTextItem(self)
        self.titleItem.node = self.node
        self.titleItem.setDefaultTextColor(NodeColor.DEFAULT_TITLE)
        self.titleItem.setFont(self.titleFont)
        self.titleItem.setPos(self.titlePadding, self.titlePadding//2)
        self.titleItem.setTextWidth(self.width - 2 * self.titlePadding)
        
    def initContent(self):
        '''節點內部文字描述'''
        self.graphicsContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            int(1.5 * self.edgeSize),
            int(self.titleHeight + self.edgeSize//2),
            int(self.width - 2.5 * self.edgeSize),
            int(self.height - 1 * self.edgeSize - self.titleHeight))
        # 影片中不知道為什麼沒轉成整數也可以運行
        # self.content.setGeometry(self.edgeSize, self.titleHeight + self.edgeSize,
                                #  self.width - 2*self.edgeSize, self.height - 2*self.edgeSize - self.titleHeight)
        self.graphicsContent.setWidget(self.content)

    def initSockets(self):
        '''節點連結點'''
        pass
        
    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        '''繪製節點圖形'''
        # 標題
        pathTitle = QPainterPath()
        pathTitle.setFillRule(Qt.FillRule.WindingFill)
        pathTitle.addRoundedRect(0, 0, self.width, self.titleHeight, self.edgeSize, self.edgeSize)
        pathTitle.addRect(0, self.titleHeight - self.edgeSize, self.edgeSize, self.edgeSize)
        pathTitle.addRect(self.width - self.edgeSize, self.titleHeight - self.edgeSize, self.edgeSize, self.edgeSize)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(NodeColor.DEFAULT_BRUSH_TITLE))
        painter.drawPath(pathTitle.simplified())
        # 描述
        pathContent = QPainterPath()
        pathContent.setFillRule(Qt.FillRule.WindingFill)
        pathContent.addRoundedRect(0, self.titleHeight, self.width, self.height - self.titleHeight, self.edgeSize, self.edgeSize)
        pathContent.addRect(0, self.titleHeight, self.edgeSize, self.edgeSize)
        pathContent.addRect(self.width - self.edgeSize, self.titleHeight, self.edgeSize, self.edgeSize)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(NodeColor.DEFAULT_BRUSH_BACKGROUND))
        painter.drawPath(pathContent.simplified())
        # 邊框
        pathOutline = QPainterPath()
        pathOutline.addRoundedRect(0, 0, self.width, self.height, self.edgeSize, self.edgeSize)
        painter.setPen(QPen(NodeColor.DEFAULT_PEN) if not self.isSelected() else QPen(NodeColor.DEFAULT_PEN_SELECTED))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(pathOutline.simplified())