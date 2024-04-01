from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView
from PyQt5.QtGui import QIcon, QMouseEvent, QPainter, QWheelEvent
from PyQt5.QtCore import Qt, QEvent

from .node_Edge import Edge
from .node_Node import Node
from .node_Socket import NodeGraphicsSocket
from .nodeEditor_Scene import Scene

from config.debug import DEBUG_MODE
from config.icon import Icon

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200 ,200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 創建圖像場景
        self.scene = Scene()
        self.addNodes()

        # 創建圖像視圖
        self.view = NodeGraphicsView(self.scene.nodeGraphicsScene, self)
        self.layout.addWidget(self.view)

        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

    def addNodes(self):
        '''新增節點'''
        # 放置初始節點
        node1 = Node(self.scene, "第一個節點", input=[1, 2, 3, 3, 2], output=[1])
        node2 = Node(self.scene, "第二個節點", input=[1, 2, 3], output=[1])
        node3 = Node(self.scene, "第三個節點", input=[1, 2, 3], output=[1])
        node1.setPos(-350, -250)
        node2.setPos(0, 0)
        node3.setPos(50, -250)

        # node1.content.addLabel("First Label")

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)

class NodeGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent)
        self.graphicsScene = graphicsScene

        self.initUI()
        self.setScene(self.graphicsScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 15  # 調整初始值
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        self.dragStartPosition = None  # 滑鼠開始拖曳位置

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
        self.dragStartPosition = event.pos()

    def middleMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠中鍵'''
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.dragStartPosition = None

    def leftMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠左鍵'''
        

        item = self.getItemAtClick(event)
        if DEBUG_MODE: print(item)
        if type(item) is NodeGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                print("Starting dragging edge")
                print("   assign Start Socket")
                return
            
        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            print("Ending dragging edge")
            if type(item) is NodeGraphicsSocket:
                print("   assign End Socket")
                return

        super().mousePressEvent(event)

        
    def rightMouseButtonPress(self, event: QMouseEvent):
        '''按下滑鼠右鍵'''
        super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠左鍵'''
        super().mouseReleaseEvent(event)
    
    def rightMouseButtonRelease(self, event: QMouseEvent):
        '''放開滑鼠右鍵'''
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
        if self.dragStartPosition:
            delta = event.pos() - self.dragStartPosition
            self.dragStartPosition = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def eventFilter(self, obj, event: QMouseEvent):
        '''事件篩選器：檢視按下的滑鼠按鈕'''
        if event.type() == QEvent.Type.MouseButtonPress:
            print("Mouse Pressed:", event.button())
        elif event.type() == QEvent.Type.MouseButtonRelease:
            print("Mouse Released:", event.button())
        return super().eventFilter(obj, event)
    
    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
