import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QFileDialog, QLabel
from PyQt5.QtGui import QIcon

from config.icon import Icon
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.filename = None

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

        # 下方狀態條
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        nodeEditor.view.scenePosChanged.connect(self.onScenePosChanged)

        self.setGeometry(200 ,200, 800, 600)
        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        '''開啟新視窗(刪除舊有全物件)'''
        self.centralWidget().scene.clear()

    def onFileOpen(self):
        '''開啟檔案'''
        fname, filter = QFileDialog.getOpenFileName(self, "開啟檔案")
        if fname == '':
            return
        elif os.path.isfile(fname):
            self.centralWidget().scene.loadFromFile(fname)

    def onFileSave(self):
        '''儲存檔案'''
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("已成功儲存檔案 %s" % self.filename)

    def onFileSaveAs(self):
        '''另存新檔'''
        fname, filter = QFileDialog.getSaveFileName(self, "另存新檔")
        if fname == '':
            return
        self.filename = fname
        self.onFileSave()

    def onEditUndo(self):
        print("Undo last operation")

    def onEditRedo(self):
        print("Redo last operation")

    def onEditDelete(self):
        print("Delete selected items")
