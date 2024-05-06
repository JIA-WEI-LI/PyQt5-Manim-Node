import os
import json
from PyQt5.QtCore import Qt, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QCloseEvent, QIcon, QFont

from .BlenderStyleWidget.window_messageBox import MessageBox
from common.style_sheet import StyleSheet
from config.icon import Icon
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorMainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.name_company = 'Blenderfreak'
        self.name_projuct = 'NodeEditor'
        self.initUI()

    # DELETED：刪除自創工具列按鈕
    # def createAct(self, name:str, shortcut:str, tooltip:str, callback):
    #     act = QAction(name, self)
    #     act.setShortcut(shortcut)
    #     act.setToolTip(tooltip)
    #     act.triggered.connect(callback)
    #     return act

    @StyleSheet.apply(StyleSheet.EDITOR_WINDOW)
    def initUI(self):
        # 隱藏最上方視窗標題列
        # self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        self.createActions()
        self.createMenus()

        # 節點畫面
        self.nodeEditor = NodeEditorWidget(self)
        self.nodeEditor.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.nodeEditor)

        self.createStatusBar()

        # self.setGeometry(200 ,200, 1960, 1280)
        self.showMaximized() 
        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setTitle()
        self.show()

    def setTitle(self):
        title = "Node Editor - "
        title += self.getCurrentNodeEditorWidget().getUserFriendlyFilename()

        self.setWindowTitle(title)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.nodeEditor.view.scenePosChanged.connect(self.onScenePosChanged)

    def createActions(self):
        self.actNew = QAction('&新增檔案', self, shortcut='Ctrl+N', statusTip="新增檔案", triggered=self.onFileNew)
        self.actOpen = QAction('&開啟檔案', self,  shortcut='Ctrl+O', statusTip="開啟檔案", triggered=self.onFileOpen)
        self.actSave = QAction('&儲存檔案', self,  shortcut='Ctrl+S', statusTip="儲存檔案", triggered=self.onFileSave)
        self.actSaveAs = QAction('&另存新檔', self,  shortcut='Ctrl+Shift+S', statusTip="另存新檔", triggered=self.onFileSaveAs)
        self.actExit = QAction('&退出', self,  shortcut='Ctrl+Q', statusTip="退出應用程式", triggered=self.close)

        self.actUndo = QAction('&上一步', self,  shortcut='Ctrl+Z', statusTip="返回上一步", triggered=self.onEditUndo)
        self.actRedo = QAction('&下一步', self,  shortcut='Ctrl+Shift+Z', statusTip="返回下一步", triggered=self.onEditRedo)
        self.actCut = QAction('&剪下', self,  shortcut='Ctrl+X', statusTip="剪下物件", triggered=self.onEditCut)
        self.actCopy = QAction('&複製', self,  shortcut='Ctrl+C', statusTip="複製物件到剪貼簿", triggered=self.onEditCopy)
        self.actPaste = QAction('&貼上', self,  shortcut='Ctrl+V', statusTip="返回下一步", triggered=self.onEditPaste)
        self.actDeleted = QAction('&刪除', self,  shortcut='Del', statusTip="刪除選擇物件", triggered=self.onEditDelete)

    def createMenus(self):
        # 主畫面選單欄選擇
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&檔案')
        self.fileMenu.setMinimumWidth(150)
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu("&編輯")
        self.editMenu.setMinimumWidth(150)
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDeleted)

    def updateMenus(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self):
        return self.getCurrentNodeEditorWidget().scene.has_been_modified
    
    def getCurrentNodeEditorWidget(self):
        return self.centralWidget()

    def maybeSave(self) -> bool:
        if not self.isModified():
            return True
        
        res = QMessageBox.warning(self, "是否確認關閉檔案？", "此文件即將被關閉，您希望另存新檔嗎？",
                                        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        if res == QMessageBox.StandardButton.Save:
            return self.onFileSave()
        elif res == QMessageBox.StandardButton.Cancel:
            return False
        
        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d] " % (x, y))

    def onFileNew(self):
        '''開啟新視窗(刪除舊有全物件)'''
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().scene.clear()
            self.filename = None
            self.setTitle()

    def onFileOpen(self):
        '''開啟檔案'''
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, "開啟檔案")
            if fname == '':
                return
            if os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().scene.loadFromFile(fname)
                self.statusBar().showMessage("已成功開啟檔案 %s" % fname)
                self.filename = fname
                self.setTitle()

    def onFileSave(self) -> bool:
        '''儲存檔案'''
        if self.filename is None: return self.onFileSaveAs()
        self.getCurrentNodeEditorWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("已成功儲存檔案 %s" % self.filename)
        
        self.setTitle()
        return True

    def onFileSaveAs(self) -> bool:
        '''另存新檔'''
        fname, filter = QFileDialog.getSaveFileName(self, "另存新檔", filter="JSON files (*.json)")
        if fname == '':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    def onEditUndo(self):
        '''返回上一步'''
        self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        '''返回下一步'''
        self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        '''刪除物件'''
        self.getCurrentNodeEditorWidget().scene.nodeGraphicsScene.views()[0].deleteSelected()

    def onEditCut(self):
        data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete = True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete = False)
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
        
        self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)

    def readSettings(self):
        settings = QSettings(self.name_company, self.name_projuct)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSetting(self):
        setting = QSettings(self.name_company, self.name_projuct)
        setting.setValue('pos', self.pos())
        setting.setValue('size', self.size())
