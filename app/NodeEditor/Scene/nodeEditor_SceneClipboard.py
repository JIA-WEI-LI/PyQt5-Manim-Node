from collections import OrderedDict
from NodeEditor.Node.node_Node import Node
from NodeEditor.Edge.node_Edge import Edge
from NodeEditor.Edge.node_GraphicsEdge import NodeGraphicsEdge

from config.debug import DebugMode

DEBUG = DebugMode.NODEEDITOR_CLIPBOARD

class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete=False):
        if DEBUG: print("-- COPY TO CLIPBOARD --")

        sel = self.scene.nodeGraphicsScene.selectedItems()
        sel_nodes, sel_edges, sel_sockets = [], [], []

        # 分類節點與連結點
        for item in self.scene.nodeGraphicsScene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    # sel_sockets[socket.id] = socket
                    sel_sockets.append(socket)
            elif isinstance(item, NodeGraphicsEdge):
                sel_edges.append(item.edge)

        if DEBUG:
            print(" NODES\n     ", sel_nodes)
            print(" EDGES\n     ", sel_edges)
            print(" SOCKETS\n     ", sel_sockets)
        
        # 移除所有未連結的線段
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                pass
            else:
                if DEBUG: print("edge ", edge, " is not connected with both sides")
        for edge in edges_to_remove:
            sel_edges.remove(edge)

        # 製作最後的線段
        edge_final = []
        for edge in sel_edges:
            edge_final.append(edge.serialize())

        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edge_final)
        ])

        if delete:
            self.scene.nodeGraphicsScene.views()[0].deleteSelected()
            self.scene.history.storeHistory("Cut out elements from scene", setModified=True)
        return data
    
    def deserializeFromClipboard(self, data):
        hashmap = {}

        view = self.scene.nodeGraphicsScene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_position

        # 計算選擇物件的中心
        minx, maxx, miny, maxy = 0, 0, 0, 0
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
        bbox_center_x = (minx + maxx)/2
        bbox_center_y = (miny + maxy)/2

        offset_x = mouse_scene_pos.x() - bbox_center_x
        offset_y = mouse_scene_pos.y() - bbox_center_y

        # 創建各個節點
        for node_data in data['nodes']:
            new_node = Node(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)

            pos = new_node.pos
            new_node.setPos(pos.x() + offset_x, pos.y() + offset_y)

        # 創建各個線段
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        self.scene.history.storeHistory("Pasted elements in scene", setModified=True)