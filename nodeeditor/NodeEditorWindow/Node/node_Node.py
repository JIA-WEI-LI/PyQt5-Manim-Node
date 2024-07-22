from collections import OrderedDict
from PyQt5.QtGui import QColor

from .node_ContentWidget import NodeContentWidget
from .node_GraphicsNode import NodeGraphicsNode
from ..Serialization.node_Serializable import Serializable
from ..Socket.node_Socket import Socket, NullSocket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from common import *

SOCKET_SPACE = 30
# DEBUG = DebugMode.NODE_NODE
DEBUG = True

class Node(Serializable):
    '''節點'''
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[], node_color:str=qconfig.get(cfg.nodeColor)):
        super().__init__()
        self.scene = scene
        self._title = title
        # HACK: 自定義節點標題顏色
        self.node_color = node_color

        self.initInnerClasses()
        self.initSetting()
        
        self.title = title
        self.scene.addNode(self)
        self.scene.nodeGraphicsScene.addItem(self.graphicsNode)

        self.inputs = []
        self.outputs = []
        self.initSockets(inputs, outputs)

    def initInnerClasses(self):
        self.content = NodeContentWidget(self)
        self.graphicsNode = NodeGraphicsNode(self)

    def initSetting(self):
        self.socketSpace = SOCKET_SPACE

        self.input_muliti_edged = False
        self.output_muliti_edged = True

    def initSockets(self, inputs, outputs, reset=True):
        if reset:
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                for socket in (self.inputs+self.outputs):
                    self.scene.graphicsScene.removeItem(socket.graphicsSocket)
                self.inputs = []
                self.outputs = []

        counter = 0
        for item in outputs:
            if item != 0:
                socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item, muliti_edges=True)
            else: socket = NullSocket(node=self, index=counter)   # HACK: 自製空連結點
            counter += 1
            self.outputs.append(socket)
        
        counter = 0
        for item in inputs:
            if item != 0:
                socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item, muliti_edges=False)
            else: socket = NullSocket(node=self, index=counter)   # HACK: 自製空連結點
            counter += 1
            
            self.inputs.append(socket)
        
    def __str__(self) -> str:
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.graphicsNode.pos()
    def setPos(self, x, y):
        '''設定節點位置'''
        self.graphicsNode.setPos(x, y)

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.graphicsNode.title = self._title

    def getSocketPosition(self, index, position, *, space:int=0, output_count:int=0) -> list[float, float]:
        '''設置連結點位置'''
        output_count = len(self.outputs) if output_count == 0 else output_count
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # BUG：如果設置底下開始，節點的編號也會從底部開始計算
            # y = self.graphicsNode.height - 3* self.graphicsNode.padding - self.graphicsNode.edgeSize - index * self.socketSpace
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode._padding + self.graphicsNode.edgeSize + (index + output_count) * (space + 1) * self.socketSpace
            if DEBUG: print(f"Node {self.__class__}\n  \
Node {self.id} ---> Pos {index} is bottom, \
y = titleHeight: {int(self.graphicsNode.titleHeight)} \
+ 2 * padding: {2*int(self.graphicsNode._padding)} \
+ edgeSize: {int(self.graphicsNode.edgeSize)} \
+ (index: {int(index)} +len(output): {int(len(self.outputs))}) \
* socketSpace: {int(self.socketSpace)}")
        else:
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode._padding + self.graphicsNode.edgeSize + index * (space + 1) * self.socketSpace
            if DEBUG: print(f"Node {self.__class__}\n  \
Node {self.id} ---> Pos {index} is top, \
y = titleHeight: {int(self.graphicsNode.titleHeight)} \
+ 2 * padding: {2*int(self.graphicsNode._padding)} \
+ edgeSize: {int(self.graphicsNode.edgeSize)} \
+ (index: {int(index)} +len(output): {int(len(self.outputs))}) \
* socketSpace: {int(self.socketSpace)}")

        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            # HACK: 因為有建立自定義空白連結點 NullSocket，所有 socket 相關皆需判斷
            if type(socket) == Socket:
                for edge in socket.edges:
                    edge.updatePositions()
    
    def remove(self):
        if DEBUG: print("> Removing Node: ", self)
        if DEBUG: print(" - remove all edge from sockets")
        for socket in (self.inputs + self.outputs):
            # HACK: 因為有建立自定義空白連結點 NullSocket，所有 socket 相關皆需判斷
            if type(socket) == Socket:
                for edge in socket.edges:
                    if DEBUG: print("    - removing from socket: ", socket, " edge: ", edge)
                    edge.remove()
        if DEBUG: print(" - remove graphicsNode: ", self)
        self.scene.nodeGraphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        if DEBUG: print(" - remove node from the scene: ", self)
        self.scene.removeNode(self)
        if DEBUG: print(" - everything was done: ", self)

    def node_type(self, type:int=1):
        # HACK: 自定義節點類型，並決定節點顏色
        try:
            self.node_color = qconfig.get(cfg.nodeColor)
        except Exception as e:
            print("node_Node:: Error number of type")

    def serialize(self):
        '''序列化資訊'''
        inputs, outputs, contents = [], [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        for content_type, content_data in self.content.contentLists:
            contents.append({'type': content_type, 'data': content_data})
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.graphicsNode.scenePos().x()),
            ('pos_y', self.graphicsNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('node_color', self.node_color),
            ('content', contents),
            ('content', contents)
            ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        '''載入序列化資訊'''
        if restore_id: self.id = data['id']
        self.outputs = data['outputs']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']
        self.node_color = data['node_color']
        
        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        self.graphicsNode.height = self.graphicsNode.titleHeight + 2* self.graphicsNode._padding

        self.inputs, self.outputs = [], []
        for socket_data in data['outputs']:
            if socket_data['id'] != 0: 
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
            else: new_socket = NullSocket(node=self, index=socket_data['index'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)
        for socket_data in data['inputs']:
            if socket_data['id'] != 0:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
            else: new_socket = NullSocket(node=self, index=socket_data['index'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)
        
        res = self.content.deserialize(data['content'], hashmap)

        return True, res