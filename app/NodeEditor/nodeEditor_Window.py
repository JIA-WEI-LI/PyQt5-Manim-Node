from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction
from PyQt5.QtGui import QIcon

from config.icon import Icon
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.initUI()

    def createAct(self, name:str, shortcut:str, tooltip:str, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        menubar = self.menuBar()

        # 主畫面選單欄選擇
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.createAct('&New', 'Ctrl+N', "Create New graph", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        fileMenu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        fileMenu.addAction(self.createAct('Save &As...', 'Ctrl+Shift+S', "Save file as ...", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('E&xit', 'Ctrl+Q', "Exit application", self.close))

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        editMenu.addAction(self.createAct('&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('&Delete', 'Del', "Delete selected items", self.onEditDelete))

        # 節點畫面
        nodeEditor = NodeEditorWidget(self)
        self.setCentralWidget(nodeEditor)

        self.setGeometry(200 ,200, 800, 600)
        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

    def onFileNew(self):
        print("On File new clicked")

    def onFileOpen(self):
        print("Open file")

    def onFileSave(self):
        print("Save file")

    def onFileSaveAs(self):
        print("Save file as ...")

    def onEditUndo(self):
        print("Undo last operation")

    def onEditRedo(self):
        print("Redo last operation")

    def onEditDelete(self):
        print("Delete selected items")
