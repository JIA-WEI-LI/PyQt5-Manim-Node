from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainter, QWheelEvent
from PyQt5.QtWidgets import QGraphicsView, QApplication
from memory_profiler import profile

from .Edge.node_Edge import Edge, EDGE_TYPE_BEZIER
from .Edge.node_GraphicsEdge import NodeGraphicsEdge
from .Node.node_Node import Node
from .Socket.node_Socket import NodeGraphicsSocket
from .Other.node_Cutline import NodeCuteline
from .nodeEditor_Scene import Scene, NodeGraphicsScene

from common.style_sheet import StyleSheet
from common.performance_utils import calculate_time
from config.debug import DebugMode, DebugTimer
from config.file_path import GRAPH_JSON_PATH

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10
DEBUG = DebugMode.NODEEDITOR_WINDOW

class NodeGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, graphicsScene: NodeGraphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initUI()
        self.setScene(self.graphicsScene)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDraggingRectangle = False

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 7  # 調整初始值
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # cutline
        self.cutline = NodeCuteline()
        self.graphicsScene.addItem(self.cutline)

        self.dragStartPosition = None  # 滑鼠開始拖曳位置

    # @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 可拖曳滑鼠選擇複數物件
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

        StyleSheet.applyStyle("editor_window", self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        '''滑鼠點擊事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        '''滑鼠放開事件'''
        if event.button() ==Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠中鍵'''
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠中鍵'''
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def leftMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠左鍵'''
        item = self.getItemAtClick(event)
        self.lastLmbClickScenePos = self.mapToScene(event.pos()) # 紀錄滑鼠初始點擊位置

        if DEBUG: print("LMB Clicked on ", item, self.debug_modifiers(event))
        
        # 使用快捷鍵選取複數物件
        if hasattr(item, "node") or isinstance(item, NodeGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.Type.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton,
                                        event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return 

        if DEBUG: print(item)
        if type(item) is NodeGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
            
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠右鍵'''
        super().mousePressEvent(event)
        
        item = self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item, NodeGraphicsEdge): print("RMB DEBUG: ", item.edge, "connecting sockets: ",
                                                         item.edge.start_socket, " <--> ", item.edge.end_socket)
            if type(item) is NodeGraphicsSocket: print("RMB DEBUG: ", item.socket, "has edge", item.socket.edges)
            
            if item is None:
                print("Scene: ")
                print("  Nodes:")
                for node in self.graphicsScene.scene.nodes: print("    ", node)
                print("  Edges:")
                for edge in self.graphicsScene.scene.edges: print("    ", edge)

        if item is None:
            # HACK: 使用滑鼠左鍵選取全物件
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
                return
            else:
                self.rubberBandDraggingRectangle = True
    
    def leftMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠左鍵'''
        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, NodeGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton,
                                        event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return 
            
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return
        
        if self.rubberBandDraggingRectangle:
            self.rubberBandDraggingRectangle = False
            if DEBUG: print(" == LMB Release: storeHistory Finish ==")
            current_selected_items = self.graphicsScene.selectedItems()
            if current_selected_items != self.graphicsScene.scene._last_selected_items:
                # self.graphicsScene.scene._last_selected_items = current_selected_items
                if current_selected_items == []:
                    self.graphicsScene.itemsDeselected.emit()
                else:
                    self.graphicsScene.itemSelected.emit()
            return

        if item is None:
            self.graphicsScene.itemsDeselected.emit()

        super().mouseReleaseEvent(event)
    
    def rightMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠右鍵'''
        # BUG: 開啟APP後先移動節點後使用切割會觸發閃退
        item = self.getItemAtClick(event)
        if DEBUG: print("-- RMB Release , Drag Mode: ", self.dragMode(), " self.node = ", self.mode)

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdge()
            self.cutline.lines_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.mode = MODE_NOOP
            if DEBUG: print("-- RMB Release Cut mode, Drag Mode: ", self.dragMode(), " self.node = ", self.mode)
            return

        if self.rubberBandDraggingRectangle:
            self.rubberBandDraggingRectangle = True
            self.graphicsScene.scene.history.storeHistory("Selection changed")
            if DEBUG: print("-- RMB Release rubberBandDraggingRectangle: ", self.rubberBandDraggingRectangle)

        if DEBUG: print("-- RMB Release 2, Drag Mode: ", self.dragMode(), " self.node = ", self.mode)
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        '''滑鼠中鍵滾論縮放視窗'''
        zoomOutFactor = 1 / self.zoomInFactor
        oldPos = self.mapToScene(event.pos())
        
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
            
        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
            
        if not clamped or self.zoomClamp is False:    
            self.scale(zoomFactor, zoomFactor)

    def mouseMoveEvent(self, event: QMouseEvent):
        '''滑鼠移動事件'''
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.nodeGraphicsEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.nodeGraphicsEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.lines_points.append(pos)
            self.cutline.update()
        
        if self.dragStartPosition:
            delta = event.pos() - self.dragStartPosition
            self.dragStartPosition = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

        # 回傳滑鼠座標
        self.last_scene_mouse_position = self.mapToScene(event.pos())
        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
        )

        # else:
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        '''鍵盤按鍵事件'''
        if event.key() == Qt.Key.Key_K:
            print(" Content children: ", len(self.graphicsScene.scene.nodes[0].content.children()))
            for node in self.graphicsScene.scene.nodes:
                vlayout = node.content.vboxLayout
                print(f"Node {node} ---> Content Layout: {vlayout},\n{' ' * 23}"
                        f"  Node graphicsNode Height: {node.graphicsNode.height}\n{' ' * 23}"
                        f"  Content Size: ({node.content.geometry().width()} , {node.content.geometry().height()})\n{' ' * 23}"
                        f"  Parent  Size: ({vlayout.parentWidget().geometry().width()} , {vlayout.parentWidget().geometry().height()})\n{' ' * 23}"
                        f"  Pos: ({vlayout.geometry().x()} , {vlayout.geometry().y()})"
                        f"  Size: ({vlayout.geometry().width()} , {vlayout.geometry().height()})"
                        f"  Item: {vlayout.count()}  Space: {vlayout.spacing()}")
        super().keyPressEvent(event)

    def cutIntersectingEdge(self):
        for ix in range(len(self.cutline.lines_points) - 1):
            p1 = self.cutline.lines_points[ix]
            p2 = self.cutline.lines_points[ix - 1]

            for edge in self.graphicsScene.scene.edges:
                if edge and edge.nodeGraphicsEdge.intersectsWith(p1, p2):
                    edge.remove()

        self.graphicsScene.scene.history.storeHistory("Delete cutted edges", setModified=True)

    def deleteSelected(self):
        '''刪除選擇物件'''
        for item in self.graphicsScene.selectedItems():
            if isinstance(item, NodeGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()
        self.graphicsScene.scene.history.storeHistory("Delete selected", setModified=True)

    def debug_modifiers(self, event: QMouseEvent):
        out = "MODS: "
        if event.modifiers() & Qt.Modifier.SHIFT: out += " SHIFT "
        if event.modifiers() & Qt.Modifier.CTRL: out += " CTRL "
        if event.modifiers() & Qt.Modifier.ALT: out += " ALT "
        return out

    def eventFilter(self, obj, event: QMouseEvent):
        '''事件篩選器：檢視按下的滑鼠按鈕'''
        if event.type() == QEvent.Type.MouseButtonPress:
            print("Mouse Pressed:", event.button())
        elif event.type() == QEvent.Type.MouseButtonRelease:
            print("Mouse Released:", event.button())
        return super().eventFilter(obj, event)
    
    def getItemAtClick(self, event):
        '''回傳點擊的物件'''
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        if DEBUG: print("View::edgeDragStart - Start dragging edge")
        if DEBUG: print("View::edgeDragStart - assign Start Socket to: ", item.socket)
        # self.previousEdge = item.socket.edge
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.graphicsScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print("View::edgeDragStart - dragEdge: ", self.drag_edge)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP

        if DEBUG: print("View::edgeDragEnd - Ending dragging edge")
        self.drag_edge.remove()
        self.drag_edge = None

        if type(item) is NodeGraphicsSocket:
            if item.socket != self.drag_start_socket:
                if not item.socket.is_multi_edges: 
                    item.socket.removeAllEdges()
                if not self.drag_start_socket.is_multi_edges:
                    self.drag_start_socket.removeAllEdges()

                new_edge = Edge(self.graphicsScene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                if DEBUG: print("View::edgeDragEnd ~ created new edge: ", new_edge, " connecting ", new_edge.start_socket, " <--> ", new_edge.end_socket)
                self.graphicsScene.scene.history.storeHistory("Created new edge by dragging", setModified=True)
                return True
        
        if DEBUG: print("View::edgeDragEnd - everything done")
        return False
    
    @calculate_time(DebugTimer.NODEEDITOR_WINDOW) 
    def distanceBetweenClickAndReleaseIsOff(self, event):
        '''確保距離上一次點擊滑鼠位置夠遠'''
        newLmbClickScenePos = self.mapToScene(event.pos())
        distScenePos = newLmbClickScenePos - self.lastLmbClickScenePos
        edgeDragThreshoilSquare = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (distScenePos.x()*distScenePos.x() + distScenePos.y()*distScenePos.y()) > edgeDragThreshoilSquare