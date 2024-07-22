import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMessageBox

from .Edge.node_Edge import Edge
from .Node.node_Node import Node
from .nodeEditor_Scene import Scene, InvalidFile
from .nodeEditor_GraphicsView import NodeGraphicsView
from NodeEditorNodes.node_Calculator import *
from NodeEditorNodes.Testing_node import Node_Test
from common import *

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

        # 創建圖像視圖
        self.view = NodeGraphicsView(self.scene.nodeGraphicsScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.isModified()

    def isFilenameSet(self):
        return self.filename is not None
    
    def getSelectedItems(self):
        return self.scene.getSelectedItems()
    
    def hasSelectedItems(self):
        return self.getSelectedItems() != []
    
    def canUndo(self):
        return self.scene.history.canUndo()
    
    def canRedo(self):
        return self.scene.history.canRedo()
    
    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")
    
    def fileNew(self):
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()

    # @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def fileLoad(self, filename):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            self.scene.history.clear()
            self.scene.history.storeInitialHistoryStamp()
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Error loading %s" % os.path.basename(filename), str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()
            StyleSheet.applyStyle("editor_window", self)

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
        node_int0 = Node_Calculator(self.scene, 0)
        
        node_int0.setPos(-100, -100)

        # edge1 = Edge(self.scene, node2.outputs[0], node1.inputs[0])
        # edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)

        self.scene.history.storeInitialHistoryStamp()