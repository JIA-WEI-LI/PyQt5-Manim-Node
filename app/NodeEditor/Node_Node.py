from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.QtGui import QColor, QPen, QFont, QBrush, QPainter, QPainterPath
from NodeEditor_Window import Scene

class Node():
    '''節點'''
    def __init__(self, scene: Scene, title="Undefined Node"):
        self.scene = scene
        self.title = title
        
        self.content = NodeContentWidget()
        self.graphicsNode = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.dmGraphicsScene.addItem(self.graphicsNode)
        
        self.input = []
        self.output = []

class NodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__initUI()
        
    def __initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
        self.label = QLabel("Some Title")
        self.vboxLayout.addWidget(self.label)
        self.vboxLayout.addWidget(QTextEdit("foo"))

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent=parent)
        self.node = node
        self.content = self.node.content
        
        self.titleColor = QColor('#fff')
        self.titleFont = QFont("Ubuntu", 10)
        
        self.width, self.height = 180, 240
        self.edgeSize = 10.0
        self.titleHeight = 24.0
        self.titlePadding = 6.0
        self.penDefault = QPen(QColor('#7F000000'))
        self.penSelected = QPen(QColor('#FFFFA637'))
        self.brushTitle = QBrush(QColor('#FF313131'))
        self.brushBackground = QBrush(QColor('#E3212121'))
        
        # init title
        self.__initTitle()
        self.title = self.node.title
        
        self.__initContent()
        
        self.__initUI()
        
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
            2 * self.edgeSize * self.width,
            2 * self.edgeSize * self.height
        ).normalized()
        
    def __initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    
    def __initTitle(self):
        self.titleItem = QGraphicsTextItem(self)
        self.titleItem.setDefaultTextColor(self.titleColor)
        self.titleItem.setFont(self.titleFont)
        self.titleItem.setPos(self.titlePadding, self.titlePadding//2)
        self.titleItem.setTextWidth(self.width - 2 * self.titlePadding)
        
    def __initContent(self):
        self.graphicsContent = QGraphicsProxyWidget(self)
        x = int(self.edgeSize)
        y = int(self.titleHeight + self.edgeSize)
        w = int(self.width - 2 * self.edgeSize)
        h = int(self.height - 2 * self.edgeSize - self.titleHeight)
        self.content.setGeometry(x, y, w, h)
        # 影片中不知道為什麼沒轉成整數也可以運行
        # self.content.setGeometry(self.edgeSize, self.titleHeight + self.edgeSize,
                                #  self.width - 2*self.edgeSize, self.height - 2*self.edgeSize - self.titleHeight)
        self.graphicsContent.setWidget(self.content)
        
    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        '''繪製節點圖形'''
        # 標題
        pathTitle = QPainterPath()
        pathTitle.setFillRule(Qt.FillRule.WindingFill)
        pathTitle.addRoundedRect(0, 0, self.width, self.titleHeight, self.edgeSize, self.edgeSize)
        pathTitle.addRect(0, self.titleHeight - self.edgeSize, self.edgeSize, self.edgeSize)
        pathTitle.addRect(self.width - self.edgeSize, self.titleHeight - self.edgeSize, self.edgeSize, self.edgeSize)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.brushTitle)
        painter.drawPath(pathTitle.simplified())
        # 描述
        pathContent = QPainterPath()
        pathContent.setFillRule(Qt.FillRule.WindingFill)
        pathContent.addRoundedRect(0, self.titleHeight, self.width, self.height - self.titleHeight, self.edgeSize, self.edgeSize)
        pathContent.addRect(0, self.titleHeight, self.edgeSize, self.edgeSize)
        pathContent.addRect(self.width - self.edgeSize, self.titleHeight, self.edgeSize, self.edgeSize)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.brushBackground)
        painter.drawPath(pathContent.simplified())
        # 邊框
        pathOutline = QPainterPath()
        pathOutline.addRoundedRect(0, 0, self.width, self.height, self.edgeSize, self.edgeSize)
        painter.setPen(self.penDefault if not self.isSelected() else self.penSelected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(pathOutline.simplified())