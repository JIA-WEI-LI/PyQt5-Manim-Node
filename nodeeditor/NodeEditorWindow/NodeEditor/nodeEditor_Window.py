import os
import json
from typing import Union
from PyQt5.QtCore import Qt, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QCloseEvent, QIcon, QFont

from common import *
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorMainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.name_company = 'Blenderfreak'
        self.name_projuct = 'NodeEditor'
        self.initUI()

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
        self.setWindowIcon(Icon(FluentIcon.IOT))
        self.setTitle()
        self.show()
        self.styleSetting()

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
        self.actNew = QAction(Icon(FluentIcon.DOCUMENT), '&新增檔案', self, shortcut='Ctrl+N', statusTip="新增檔案", triggered=self.onFileNew)
        self.actOpen = QAction('&開啟檔案', self,  shortcut='Ctrl+O', statusTip="開啟檔案", triggered=self.onFileOpen)
        self.actSave = QAction(Icon(FluentIcon.SAVE),'&儲存檔案', self,  shortcut='Ctrl+S', statusTip="儲存檔案", triggered=self.onFileSave)
        self.actSaveAs = QAction(Icon(FluentIcon.SAVE_AS), '&另存新檔', self,  shortcut='Ctrl+Shift+S', statusTip="另存新檔", triggered=self.onFileSaveAs)
        self.actExit = QAction(Icon(FluentIcon.CLOSE), '&退出', self,  shortcut='Ctrl+Q', statusTip="退出應用程式", triggered=self.close)

        self.actUndo = QAction('&上一步', self,  shortcut='Ctrl+Z', statusTip="返回上一步", triggered=self.onEditUndo)
        self.actRedo = QAction('&下一步', self,  shortcut='Ctrl+Shift+Z', statusTip="返回下一步", triggered=self.onEditRedo)
        self.actCut = QAction(Icon(FluentIcon.CUT), '&剪下', self,  shortcut='Ctrl+X', statusTip="剪下物件", triggered=self.onEditCut)
        self.actCopy = QAction(Icon(FluentIcon.COPY), '&複製', self,  shortcut='Ctrl+C', statusTip="複製物件到剪貼簿", triggered=self.onEditCopy)
        self.actPaste = QAction(Icon(FluentIcon.PASTE), '&貼上', self,  shortcut='Ctrl+V', statusTip="返回下一步", triggered=self.onEditPaste)
        self.actDeleted = QAction(Icon(FluentIcon.DELETE), '&刪除', self,  shortcut='Del', statusTip="刪除選擇物件", triggered=self.onEditDelete)

    def createMenus(self):
        # 主畫面選單欄選擇
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&檔案')
        self.fileMenu.setMinimumWidth(200)
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu("&編輯")
        self.editMenu.setMinimumWidth(200)
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
        return self.getCurrentNodeEditorWidget().scene.isModified()
    
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

    def getFileDialogDirectory(self):
        """Returns starting directory for ``QFileDialog`` file open/save"""
        return ''

    def getFileDialogFilter(self):
        """Returns ``str`` standard file open/save filter for ``QFileDialog``"""
        return 'Graph (*.json);;All files (*)'

    def onFileNew(self):
        '''開啟新視窗(刪除舊有全物件)'''
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().fileNew()
            self.setTitle()

    def onFileOpen(self):
        '''開啟檔案'''
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, "開啟檔案", self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname != '' and os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().fileLoad(fname)
                self.setTitle()

    def onFileSave(self) -> bool:
        '''儲存檔案'''
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.isFilenameSet(): return self.onFileSaveAs()
            current_nodeeditor.fileSave()
            self.statusBar().showMessage("已成功儲存檔案 %s" % current_nodeeditor.filename, 5000)

            # HACK: 支援 MDI
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True

    def onFileSaveAs(self) -> bool:
        '''另存新檔'''
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, "另存新檔", self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname == '': return False

            self.onBeforeSaveAs(current_nodeeditor, fname)
            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("已成功另存新檔 %s" % current_nodeeditor.filename, 5000)
            
            # HACK: 支援 MDI
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True
        
    def onBeforeSaveAs(self, current_nodeeditor: 'NodeEditorWidget', filename: str):
        """
        Event triggered after choosing filename and before actual fileSave(). We are passing current_nodeeditor because
        we will loose focus after asking with QFileDialog and therefore getCurrentNodeEditorWidget will return None
        """
        pass

    def onEditUndo(self):
        '''返回上一步'''
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        '''返回下一步'''
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        '''刪除物件'''
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.nodeGraphicsScene.views()[0].deleteSelected()

    def onEditCut(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete = True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete = False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getCurrentNodeEditorWidget():
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

    def styleSetting(self, qss_path:Union[str, StyleSheet]=StyleSheet.EDIORTWINDOW):
        """
        Apply a QSS stylesheet to the current widget. By default, applies the EDIORTWINDOW stylesheet.

        Parameters
        ----------
        qss_path : Union[str, StyleSheet], optional
            The path to the QSS file or a StyleSheet enum. If a string path is provided,
            it will be used as the custom path for the stylesheet. If not provided,
            the EDIORTWINDOW stylesheet will be applied. Default is StyleSheet.EDIORTWINDOW.

        Raises
        ------
        FileNotFoundError
            If the QSS file at the provided path does not exist.
        """
        if qss_path == StyleSheet.EDIORTWINDOW:
            StyleSheet.EDIORTWINDOW.apply(self)
        else:
            custom_stylesheet = StyleSheet.EMPTY
            custom_stylesheet.setPath(qss_path)
            try:
                custom_stylesheet.apply(self)
            except FileNotFoundError:
                print(f"QSS file not found: {custom_stylesheet.path()}")