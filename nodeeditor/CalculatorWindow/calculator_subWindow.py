from PyQt5.QtCore import Qt, QDataStream, QIODevice
from PyQt5.QtGui import QContextMenuEvent, QDragEnterEvent, QPixmap, QIcon
from PyQt5.QtWidgets import QGraphicsProxyWidget, QMenu, QAction

from NodeEditorWindow.NodeEditor.nodeEditor_Widget import NodeEditorWidget
from NodeEditorNodes.node_Calculator import *
from NodeEditorWindow.Edge.node_Edge import EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
from common.utils import dumpException
from .calculator_config import *\

DEBUG = True

class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setTitle()

        self.initNewNodeActions()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterlisteners(self.onDragEnter)
        self.scene.addDropListeners(self.onDrop)

        self._close_event_listeners = []

    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return Node
        return get_class_from_opcode(data['op_code'])
    
    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            node = CALC_NODES[key] 
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)
    
    def initNodeContextMenu(self):
        context_menu = QMenu(self)
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys: context_menu.addAction(self.node_actions[key])
        return context_menu

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def onDrop(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.nodeGraphicsScene.views()[0].mapToScene(mouse_position)

            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
            except Exception as e:
                dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG: print("calc_sunWindow:: ", item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e: dumpException(e)

    def handleNodeContextMenu(self, event):
        if DEBUG: print("CONTEXT: NODE")
        
        context_menu = QMenu(self)
        markDirtytAct = context_menu.addAction("Mark Dirty")
        markInvalidAct = context_menu.addAction("Mark Invalid")
        directAct = context_menu.addAction("Unmark Invalid")
        directAct = context_menu.addAction("Eval")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        if DEBUG: print("got item", selected)

    def handleEdgeContextMenu(self, event):
        if DEBUG: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        beziertAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == beziertAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
    
    def handleNewNodeContextMenu(self, event):
        if DEBUG: print("CONTEXT: EMPTY SPACE")
        context_menu = self.initNodeContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        # BUG: 使用選單後第二次點擊會移動到第一次點擊結束位置
        if action is not None:
            new_calc_node = get_class_from_opcode(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_pos.x(), scene_pos.y())
            if DEBUG: print("Selected node: ", new_calc_node)