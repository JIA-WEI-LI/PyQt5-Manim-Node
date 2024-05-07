import os
from PyQt5.QtCore import Qt, QSignalMapper, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QWidget, QMdiArea, QListWidget, QDockWidget, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QCloseEvent, QKeySequence, QBrush, QColor

from common.utils import dumpException
from common.style_sheet import StyleSheet
from .calaulator_subWindow import CalculatorSubWindow
from NodeEditorWindow import NodeEditorMainWindow

class CalculatorMainWindow(NodeEditorMainWindow):
    @StyleSheet.apply("nodeeditor\\CalculatorWindow\\qss\\calculator_window.qss")
    def initUI(self):
        self.name_company = 'Blenderfreak'
        self.name_projuct = 'Calaulator NodeEditor'

        self.mdiArea=  QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.ViewMode.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        # HACK: 調整背景顏色
        self.mdiArea.setBackground(QBrush(QColor(20, 20, 20, 80)))
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.createNodesDock()

        self.readSettings()
        self.setWindowTitle("Calaulator Example")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSetting()
            event.accept()

    def createActions(self):
        super().createActions()

        self.actClose = QAction("&關閉子視窗", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("關閉&全視窗", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&磚瓦式分割", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&瀑布式分割", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("&下一視窗", self, shortcut=QKeySequence.StandardKey.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPreviewous = QAction("&上一視窗", self, shortcut=QKeySequence.StandardKey.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)
        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&關於", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.show()
        except Exception as e: dumpException(e)

    # DELETED
    # def onFileSave(self):
    #     '''儲存檔案'''
    #     current_nodeeditor = self.getCurrentNodeEditorWidget()
    #     if current_nodeeditor:
    #         if not current_nodeeditor.isFilenameSet():
    #             return self.onFileSaveAs()
    #         else:
    #             current_nodeeditor.fileSave()   # HACK:不傳遞任何參數，保持原檔案名稱儲存
    #             self.statusBar().showMessage("已成功儲存檔案 %s" % current_nodeeditor.filename, 5000)
    #             current_nodeeditor.setTitle()
    #             return True

    # DELETED
    # def onFileSaveAs(self):
    #     '''另存新檔'''
    #     current_nodeeditor = self.activeMdiChild()
    #     if current_nodeeditor is not None:
    #         fname, filter = QFileDialog.getSaveFileName(self, "另存新檔", filter="JSON files (*.json)")
    #         if fname == '': return False
    #         current_nodeeditor.fileSave(fname)
    #         current_nodeeditor.setTitle()
    #         self.statusBar().showMessage("已成功儲存檔案 %s" % fname)
    #         return True

    def onFileOpen(self):
        '''開啟檔案'''
        fnames, filter = QFileDialog.getOpenFileNames(self, "開啟檔案")
        
        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        nodeeditor = CalculatorSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.mdiArea.addSubWindow(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)
    
    # @StyleSheet.apply("nodeeditor\\CalculatorWindow\\qss\\calculator_window.qss")
    def about(self):
        QMessageBox.about(self, "關於計算器節點編輯器範例",
                          "此 <b>計算器節點編輯器</b> 範例在於如何使用雙介面演示 PyQt5 和 節點編輯器，相關訊息可以參閱： "
                          "<a href='https://github.com/JIA-WEI-LI/PyQt5-Manim-Node'>Manim Community 節點編輯器</a>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&視窗")
        self.windowMenu.setMinimumWidth(150)
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu('&幫助')
        self.helpMenu.addAction(self.actAbout)
        self.helpMenu.setMinimumWidth(150)

    def updateMenus(self):
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)
        
        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPreviewous.setEnabled(hasMdiChild)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPreviewous)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows)!=0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i+1, child.getUserFriendlyFilename())
            if i<9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.listWidget = QListWidget()
        self.listWidget.addItem("Add")
        self.listWidget.addItem("Substract")
        self.listWidget.addItem("Multiply")
        self.listWidget.addItem("Divide")

        self.items = QDockWidget("Nodes")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.items)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self):
        nodeeditor = CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        return subwnd
    
    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None
    
    # DELETED
    # def activeMdiChild(self):
    #     """回傳 NodeEditorWidget"""
    #     activeSubWindow = self.mdiArea.activeSubWindow()
    #     if activeSubWindow:
    #         return activeSubWindow.widget()
    #     return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)