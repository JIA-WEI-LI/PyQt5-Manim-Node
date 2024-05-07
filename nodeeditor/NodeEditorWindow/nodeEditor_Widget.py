import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMessageBox

from .Edge.node_Edge import Edge
from .Node.node_Node import Node
from .nodeEditor_Scene import Scene, InvalidFile
from .nodeEditor_GraphicsView import NodeGraphicsView

from config.debug import DebugMode, DebugTimer
from common.style_sheet import StyleSheet
from NodeEditorNodes.node_Calculator import *
from NodeEditorNodes.Testing_node import Node_Test

class NodeEditorWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.filename = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 創建圖像場景
        self.scene = Scene()
        self.addNodes()

        # 創建圖像視圖
        self.view = NodeGraphicsView(self.scene.nodeGraphicsScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.has_been_modified

    def isFilenameSet(self):
        return self.filename is not None
    
    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

        return False
    
    def fileSave(self, filename=None):
        if filename is not None: self.filename = filename
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True

    def addNodes(self):
        '''新增節點'''
        # 放置初始節點
        node_int0 = Node_Integer(self.scene)
        node_str = Node_String(self.scene)
        node_Normalize = Node_Normalize(self.scene)
        node_ValueToString = Node_ValueToString(self.scene)
        node_StringToValue = Node_StringToValue(self.scene)
        node1 = Node_Add(self.scene)
        node2 = Node_Substract(self.scene)
        node3 = Node_Multiply(self.scene)
        node4 = Node_Divide(self.scene)
        node_Test = Node_Test(self.scene)
        
        node_int0.setPos(-100, -100)
        node_str.setPos(-150, -150)
        node_Normalize.setPos(-200, -200)
        node_ValueToString.setPos(-250, -250)
        node_StringToValue.setPos(-300, -300)
        node1.setPos(0, 0)
        node2.setPos(100, 100)
        node3.setPos(200, 200)
        node4.setPos(300, 300)
        node_Test.setPos(600, 0)

        # edge1 = Edge(self.scene, node2.outputs[0], node1.inputs[0])
        # edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)