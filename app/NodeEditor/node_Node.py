from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtWidgets import QCheckBox, QGraphicsSceneMouseEvent, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QSizePolicy
from PyQt5.QtGui import QPen, QFont, QBrush, QPainter, QPainterPath

from .node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from .nodeEditor_Scene import Scene

from config.debug import DebugMode
from config.palette import NodeColor

class Node():
    '''節點'''
    def __init__(self, scene:Scene, title="Undefined Node", input=[], output=[]):
        self.scene = scene
        self.title = title
        self.input = input
        self.output = output
        self.socketSpace = 22   # 連結點之間空間
        
        self.content = NodeContentWidget()
        self.graphicsNode = NodeGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.nodeGraphicsScene.addItem(self.graphicsNode)

        self.inputs = []
        self.outputs = []
        counter = 0
        for item in output:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

            self.content.addLabel(f"輸出點{counter}", isOutput=True)
        self.content.vboxLayout.addSpacing(5)
        
        counter = 0
        for item in input:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

            # self.content.addLabel(f"輸入點{counter}")
            self.content.addCheckbox(f"輸入點{counter}")
            
    def __str__(self) -> str:
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.graphicsNode.pos()
    def setPos(self, x, y):
        '''設定節點位置'''
        self.graphicsNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        '''設置連結點位置'''
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # 如果設置底下開始，節點的編號也會從底部開始計算
            y = self.graphicsNode.height - 2* self.graphicsNode.padding - self.graphicsNode.edgeSize - index * self.socketSpace
        else:
            y = self.graphicsNode.titleHeight + self.graphicsNode.padding + self.graphicsNode.edgeSize + index * self.socketSpace

        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()  

class NodeContentWidgetDefault(QWidget):
    '''預設文字介紹'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initUI()
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
        self.label = QLabel("Some Title")
        self.vboxLayout.addWidget(self.label)
        self.vboxLayout.addWidget(QTextEdit("foo"))

class NodeContentWidget(QWidget):
    '''自製內部元件構造'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.socketSpace = 16
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
    def addLabel(self, text, isOutput=False):
        label = QLabel(self)
        label.setText(text)
        label.setStyleSheet("color: white;")
        label.setFixedHeight(self.socketSpace)
        if isOutput: label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.vboxLayout.addWidget(label)
        return label
    
    def addButton(self, text):
        button = QPushButton(self)
        button.setText(text)
        button.setStyleSheet("color: white; border: none; background-color: #333; border-radius: 10px; border-bottom: 2px solid #111;")
        button.setFixedHeight(self.socketSpace)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(button)
        return button
    
    def addCheckbox(self, text, isOutput=False):
        hLayoutBox = QHBoxLayout()
        checkbox = QCheckBox()
        label = QLabel()
        hLayoutBox.setContentsMargins(0, 0, 0, 0)
        hLayoutBox.addWidget(checkbox, stretch=1) if isOutput else hLayoutBox.addWidget(checkbox)
        hLayoutBox.addWidget(label) if isOutput else hLayoutBox.addWidget(label, stretch=1)

        self.vboxLayout.addLayout(hLayoutBox)
        return checkbox, label

class NodeGraphicsNode(QGraphicsItem):
    def __init__(self, node:Node ,parent=None):
        super().__init__(parent=parent)
        self.node = node
        self.content = self.node.content
        
        self.titleFont = QFont("Ubuntu", 10)
        
        self.width = 180  # 節點寬高
        # self.height = 240
        self.padding = 4.0                  # 連結點位置出血區
        self.edgeSize = 10.0
        self.titleHeight = 24.0
        self.titlePadding = 6.0

        # 節點高度隨輸入與輸出點多寡改變
        self.height = self.titleHeight + 2 * self.padding + self.edgeSize + (len(self.node.input) + len(self.node.output)) * self.node.socketSpace
        
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
        self.titleItem.setDefaultTextColor(NodeColor.DEFAULT_TITLE)
        self.titleItem.setFont(self.titleFont)
        self.titleItem.setPos(self.titlePadding, self.titlePadding//2)
        self.titleItem.setTextWidth(self.width - 2 * self.titlePadding)
        
    def initContent(self):
        '''節點內部文字描述'''
        self.graphicsContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            int(self.edgeSize),
            int(self.titleHeight + self.edgeSize),
            int(self.width - 2 * self.edgeSize),
            int(self.height - 2 * self.edgeSize - self.titleHeight))
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