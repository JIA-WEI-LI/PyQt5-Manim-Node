from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy

from .node_GraphicsNode import NodeGraphicsNode
from ..Socket.node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from ..nodeEditor_Scene import Scene

from common.style_sheet import StyleSheet
from components.custom_checkbox import CheckBox
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class Node():
    '''節點'''
    def __init__(self, scene:Scene, title="Undefined Node", input=[], output=[]):
        self.scene = scene
        self.title = title
        self.input = input
        self.output = output
        self.socketSpace = SOCKET_SPACE   # 連結點之間空間
        
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

            self.content.addLabel(f"Output {counter}", isOutput=True)
        
        counter = 0
        for item in input:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            if item == 1: 
                self.content.addCheckbox(f"Input {counter}")
            else: self.content.addLabel(f"Input {counter}")
            
            self.inputs.append(socket)

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
            # y = self.graphicsNode.height - 3* self.graphicsNode.padding - self.graphicsNode.edgeSize - index * self.socketSpace
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode.padding + self.graphicsNode.edgeSize + (index + len(self.output)) * self.socketSpace
        else:
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode.padding + self.graphicsNode.edgeSize + index * self.socketSpace

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
        self.socketSpace = SOCKET_SPACE-7
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
    @StyleSheet.apply(StyleSheet.NODE_NODE)
    def addLabel(self, text, isOutput=False):
        label = QLabel(self)
        label.setObjectName("contentLabel")
        
        label.setText(text)
        label.setFixedHeight(self.socketSpace)
        if isOutput: label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)
        
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        
        return label
    
    def addButton(self, text):
        button = QPushButton(self)
        button.setText(text)
        button.setFixedHeight(self.socketSpace)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(button)
        
        if DEBUG: button.setStyleSheet("color: white; border: 1px solid red;")
        
        return button
    
    def addCheckbox(self, text, isOutput=False):
        hLayoutBox = QHBoxLayout()
        checkbox = CheckBox()
        label = QLabel(text)
        label.setObjectName("checkboxLabel")
        
        checkbox.setFixedHeight(self.socketSpace)
        label.setFixedHeight(self.socketSpace)
        hLayoutBox.setContentsMargins(0, 0, 0, 0)
        hLayoutBox.addWidget(checkbox, stretch=1) if isOutput else hLayoutBox.addWidget(checkbox)
        hLayoutBox.addWidget(label) if isOutput else hLayoutBox.addWidget(label, stretch=1)
        self.vboxLayout.addLayout(hLayoutBox)
        
        if DEBUG: checkbox.setStyleSheet("border: 1px solid red;")
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        
        return checkbox, label
    
    def setFixedHeightForAll(self):
        total_height = self.vboxLayout.sizeHint().height()  # 獲取 vBoxLayout 的總高度
        item_count = self.vboxLayout.count()  # 獲取 vBoxLayout 中元素的數量
        if item_count == 0:
            return
        avg_height = total_height // item_count  # 計算平均高度

        # 將每個元素的高度設置為平均高度
        for i in range(item_count):
            item_widget = self.vboxLayout.itemAt(i).widget()
            if item_widget is not None:
                item_widget.setFixedHeight(avg_height)