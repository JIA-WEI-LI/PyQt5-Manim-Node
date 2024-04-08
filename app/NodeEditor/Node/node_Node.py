from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

from .node_ContentWidget import NodeContentWidget
from .node_GraphicsNode import NodeGraphicsNode
from ..Socket.node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from ..nodeEditor_Scene import Scene
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

            if item == 1: 
                self.content.addCheckbox(f"Output {counter}")
            elif item == 2:
                self.content.addComboBox()
            elif item == 3:
                self.content.addLabel(f"Output {counter}", isOutput=True)
            elif item == 4:
                self.content.addProgressBar()
            elif item == 5:
                self.content.addPushButton(f"Output button {counter}")
            elif item == 6:
                self.content.addLineEdit(f"Onput {counter}")
            else: self.content.addLabel(f"Onput {counter}")
        
        counter = 0
        for item in input:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            if item == 1: 
                self.content.addCheckbox(f"Output {counter}")
            elif item == 2:
                self.content.addComboBox()
            elif item == 3:
                self.content.addLabel(f"Output {counter}")
            elif item == 4:
                self.content.addProgressBar()
            elif item == 5:
                self.content.addPushButton(f"Output button {counter}")
            elif item == 6:
                self.content.addLineEdit(f"Onput {counter}")
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
    
    def remove(self):
        if DEBUG: print("> Removing Node: ", self)
        if DEBUG: print(" - remove all edge from sockets")
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                if DEBUG: print("    - removing from socket: ", socket, " edge: ", socket.edge)
                socket.edge.remove()
        if DEBUG: print(" - remove graphicsNode: ", self)
        self.scene.nodeGraphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        if DEBUG: print(" - remove node from the scene: ", self)
        self.scene.removeNode(self)
        if DEBUG: print(" - everything was done: ", self)

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