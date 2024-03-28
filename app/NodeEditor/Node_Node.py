from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.QtGui import QPen, QFont, QBrush, QPainter, QPainterPath

from .node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP
from .nodeEditor_Scene import Scene

from config.palette import NodeColor

class Node():
    '''節點'''
    def __init__(self, scene:Scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        
        self.content = NodeContentWidget()
        self.graphicsNode = NodeGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.dmGraphicsScene.addItem(self.graphicsNode)
        
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP)
            counter += 1
            self.inputs.append(socket)
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width
        y = index * 20

        return x, y

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

class NodeGraphicsNode(QGraphicsItem):
    def __init__(self, node:Node, parent=None):
        super().__init__(parent=parent)
        self.node = node
        self.content = self.node.content
        
        self.titleFont = QFont("Ubuntu", 10)
        
        self.width, self.height = 180, 240
        self.edgeSize = 10.0
        self.titleHeight = 24.0
        self.titlePadding = 6.0
        
        # 標題
        self.initTitle()
        self.title = self.node.title
        
        # 連結點
        self.initSockets()

        # 內部元素
        self.initContent()
        
        self.initUI()
        
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
        self.titleItem.setDefaultTextColor(NodeColor.DEFAULT_TITLE)
        self.titleItem.setFont(self.titleFont)
        self.titleItem.setPos(self.titlePadding, self.titlePadding//2)
        self.titleItem.setTextWidth(self.width - 2 * self.titlePadding)
        
    def initContent(self):
        '''節點內部文字描述'''
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