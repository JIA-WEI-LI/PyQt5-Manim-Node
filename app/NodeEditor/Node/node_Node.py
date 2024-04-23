from collections import OrderedDict

from .node_ContentWidget import NodeContentWidget
from .node_GraphicsNode import NodeGraphicsNode
from ..Serialization.node_Serializable import Serializable
from ..Socket.node_Socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class Node(Serializable):
    '''節點'''
    def __init__(self, scene, title="Undefined Node", input=[], output=[]):
        super().__init__()
        self.scene = scene
        self._title = title
        self.input = input
        self.output = output
        self.socketSpace = SOCKET_SPACE   # 連結點之間空間
        
        self.content = NodeContentWidget(self)
        self.graphicsNode = NodeGraphicsNode(self)
        self.title = title
        self.scene.addNode(self)
        self.scene.nodeGraphicsScene.addItem(self.graphicsNode)

        self.inputs = []
        self.outputs = []
        counter = 0
        for item in output:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)
        
        counter = 0
        for item in input:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
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

    def getSocketPosition(self, index, position, *, space:int=0) -> list[float, float]:
        '''設置連結點位置'''
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.graphicsNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # 如果設置底下開始，節點的編號也會從底部開始計算
            # y = self.graphicsNode.height - 3* self.graphicsNode.padding - self.graphicsNode.edgeSize - index * self.socketSpace
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode.padding + self.graphicsNode.edgeSize + (index + len(self.output)) * (space + 1) * self.socketSpace
            if DEBUG: print(f" ---> Pos {index} is bottom, \
y = titleHeight: {int(self.graphicsNode.titleHeight)} \
+ 2 * padding: {2*int(self.graphicsNode.padding)} \
+ edgeSize: {int(self.graphicsNode.edgeSize)} \
+ (index: {int(index)} +len(output): {int(len(self.output))}) \
* socketSpace: {int(self.socketSpace)}")
        else:
            y = self.graphicsNode.titleHeight + 2* self.graphicsNode.padding + self.graphicsNode.edgeSize + index * (space + 1) * self.socketSpace
            if DEBUG: print(f" ---> Pos {index} is top, \
y = titleHeight: {int(self.graphicsNode.titleHeight)} \
+ 2 * padding: {2*int(self.graphicsNode.padding)} \
+ edgeSize: {int(self.graphicsNode.edgeSize)} \
+ (index: {int(index)} +len(output): {int(len(self.output))}) \
* socketSpace: {int(self.socketSpace)}")

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

    def serialize(self):
        '''序列化資訊'''
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.graphicsNode.scenePos().x()),
            ('pos_y', self.graphicsNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
            ])
    
    def deserialize(self, data, hashmap={}, restore_id=True):
        '''載入序列化資訊'''
        if restore_id: self.id = data['id']
        self.output = data['outputs']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])

        self.title = data['title']
        
        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        self.graphicsNode.height = self.graphicsNode.titleHeight + 2 * self.graphicsNode.padding + len(data['inputs'] + data['outputs']) * self.socketSpace

        self.inputs, self.outputs = [], []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)
        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)

        self.content.deserialize(data['content'], hashmap)

        return True