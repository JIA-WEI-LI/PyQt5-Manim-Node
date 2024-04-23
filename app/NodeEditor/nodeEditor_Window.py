import os
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QFont

from common.style_sheet import StyleSheet
from config.icon import Icon
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.initUI()

        self.filename = None

    def createAct(self, name:str, shortcut:str, tooltip:str, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def initUI(self):
        font = QFont()
        font.setPointSize(10)

        menubar = self.menuBar()
        menubar.setFont(font)

        # 主畫面選單欄選擇
        fileMenu = menubar.addMenu('&檔案')
        fileMenu.addAction(self.createAct('&新增檔案', 'Ctrl+N', "新增檔案", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&開啟檔案', 'Ctrl+O', "開啟檔案", self.onFileOpen))
        fileMenu.addAction(self.createAct('&儲存檔案', 'Ctrl+S', "儲存檔案", self.onFileSave))
        fileMenu.addAction(self.createAct('&另存新檔', 'Ctrl+Shift+S', "另存新檔", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&退出', 'Ctrl+Q', "退出應用程式", self.close))

        editMenu = menubar.addMenu("&編輯")
        editMenu.addAction(self.createAct('&上一步', 'Ctrl+Z', "返回上一步", self.onEditUndo))
        editMenu.addAction(self.createAct('&下一步', 'Ctrl+Shift+Z', "返回下一步", self.onEditRedo))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('&剪下', 'Ctrl+X', "剪下物件", self.onEditCut))
        editMenu.addAction(self.createAct('&複製', 'Ctrl+C', "複製物件到剪貼簿", self.onEditCopy))
        editMenu.addAction(self.createAct('&貼上', 'Ctrl+V', "返回下一步", self.onEditPaste))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct('&刪除', 'Del', "刪除選擇物件", self.onEditDelete))

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
        self.status_mouse_pos.setText("Scene Pos: [%d, %d] " % (x, y))

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
            self.statusBar().showMessage("已成功開啟檔案 %s" % fname)

    def onFileSave(self):
        '''儲存檔案'''
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("已成功儲存檔案 %s" % self.filename)

    def onFileSaveAs(self):
        '''另存新檔'''
        fname, filter = QFileDialog.getSaveFileName(self, "另存新檔", filter="JSON files (*.json)")
        if fname == '':
            return
        self.filename = fname
        self.onFileSave()

    def onEditUndo(self):
        '''返回上一步'''
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        '''返回下一步'''
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        '''刪除物件'''
        self.centralWidget().scene.nodeGraphicsScene.views()[0].deleteSelected()

    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete = False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete = True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()
        
        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("\033[93m Pasting og not valid json data!\033[0m")
            return
        
        if 'nodes' not in data:
            print("JSON doesnot contain any node!")
            return
        
        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)