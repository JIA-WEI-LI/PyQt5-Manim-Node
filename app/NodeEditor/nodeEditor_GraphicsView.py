from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainter, QWheelEvent
from PyQt5.QtWidgets import QGraphicsView, QApplication

from .Edge.node_Edge import Edge, EDGE_TYPE_BEZIER
from .Edge.node_GraphicsEdge import NodeGraphicsEdge
from .Node.node_Node import Node
from .Socket.node_Socket import NodeGraphicsSocket
from .Other.node_cutline import NodeCuteline
from .nodeEditor_Scene import Scene, NodeGraphicsScene

from common.style_sheet import StyleSheet
from common.performance_utils import calculate_time
from config.debug import DebugMode, DebugTimer
from config.file_path import SerializationPath

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10
DEBUG = DebugMode.NODEEDITOR_WINDOW

class NodeGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene: NodeGraphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initUI()
        self.setScene(self.graphicsScene)

        self.mode = MODE_NOOP
        self.editingFlag = False

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 7  # 調整初始值
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # cutline
        self.cutline = NodeCuteline()
        self.graphicsScene.addItem(self.cutline)

        self.dragStartPosition = None  # 滑鼠開始拖曳位置

    @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 可拖曳滑鼠選擇複數物件
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

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
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        if DEBUG: print("Press Drag Mode: ", self.dragMode())
        self.dragStartPosition = event.pos()

    def middleMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠中鍵'''
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        QApplication.restoreOverrideCursor()
        if DEBUG: print("Release Drag Mode: ", self.dragMode())
        self.dragStartPosition = None

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
            if type(item) is NodeGraphicsSocket: print("RMB DEBUG: ", item.socket, "has edge", item.socket.edge)
            
            if item is None:
                print("Scene: ")
                print("  Nodes:")
                for node in self.graphicsScene.scene.nodes: print("    ", node)
                print("  Edges:")
                for edge in self.graphicsScene.scene.edges: print("    ", edge)

        if item is None:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
                return
    
    def leftMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠左鍵'''
        item = self.getItemAtClick(event)

        # 使用快捷鍵選取複數物件
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

        super().mouseReleaseEvent(event)
    
    def rightMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠右鍵'''
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdge()
            self.cutline.lines_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.mode = MODE_NOOP
            return

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
            self.dragEdge.nodeGraphicsEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.nodeGraphicsEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.lines_points.append(pos)
            self.cutline.update()
        
        if self.dragStartPosition:
            delta = event.pos() - self.dragStartPosition
            self.dragStartPosition = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        '''鍵盤按鍵事件'''
        if event.key() == Qt.Key.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key.Key_S and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.graphicsScene.scene.saveToFile(SerializationPath.GRAPH_JSON)
        elif event.key() == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.graphicsScene.scene.loadFromFile(SerializationPath.GRAPH_JSON)
        else:
            super().keyPressEvent(event)

    def cutIntersectingEdge(self):
        for ix in range(len(self.cutline.lines_points) - 1):
            p1 = self.cutline.lines_points[ix]
            p2 = self.cutline.lines_points[ix - 1]

            for edge in self.graphicsScene.scene.edges:
                if edge.nodeGraphicsEdge.intersectsWith(p1, p2):
                    edge.remove()

    def deleteSelected(self):
        '''刪除選擇物件'''
        for item in self.graphicsScene.selectedItems():
            if isinstance(item, NodeGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

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
        self.previousEdge = item.socket.edge
        self.lastStartSocket = item.socket
        self.dragEdge = Edge(self.graphicsScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print("View::edgeDragStart - dragEdge: ", self.dragEdge)

    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP
        if type(item) is NodeGraphicsSocket:
            if item.socket != self.lastStartSocket:
                if DEBUG: print("View::edgeDragEnd -   - , previous End Socket:", self.previousEdge)
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if DEBUG: print("View::edgeDragEnd - assign End Socket", item.socket)
                if self.previousEdge is not None: self.previousEdge.remove()
                if DEBUG: print("View::edgeDragEnd - previousEdge edge remove")
                self.dragEdge.start_socket = self.lastStartSocket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                if DEBUG: print("View::edgeDragEnd - reassigned start & end sockets to drag edge", item.socket)
                self.dragEdge.updatePositions()
                return True
        
        # if self.dragEdge is not None: pass  # 檢查 self.dragEdge 是否為 None
        if DEBUG: print("View::edgeDragEnd - Ending dragging edge")
        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print("View::edgeDragEnd - everything done")
        return False
    
    @calculate_time(DebugTimer.NODEEDITOR_WINDOW) 
    def distanceBetweenClickAndReleaseIsOff(self, event):
        '''確保距離上一次點擊滑鼠位置夠遠'''
        newLmbClickScenePos = self.mapToScene(event.pos())
        distScenePos = newLmbClickScenePos - self.lastLmbClickScenePos
        edgeDragThreshoilSquare = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (distScenePos.x()*distScenePos.x() + distScenePos.y()*distScenePos.y()) > edgeDragThreshoilSquare