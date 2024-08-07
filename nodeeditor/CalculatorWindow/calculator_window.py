import os
from pprint import PrettyPrinter
from PyQt5.QtCore import Qt, QSignalMapper, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QWidget, QMdiArea, QListWidget, QDockWidget, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QCloseEvent, QKeySequence, QBrush, QColor, QIcon

from common.utils import dumpException
from common.style_sheet import StyleSheet, setStyleSheet
from .calculator_subWindow import CalculatorSubWindow
from .calculator_dragListBox import NodeGraphicsDragListBox
from NodeEditorWindow import NodeEditorMainWindow

from CalculatorWindow.calculator_config_nodes import *
from CalculatorWindow.calculator_config import *
from CalculatorWindow.calculator_node_base import *

DEBUG = False

class CalculatorMainWindow(NodeEditorMainWindow):
    def initUI(self):
        self.name_company = 'Blenderfreak'
        self.name_projuct = 'Calaulator NodeEditor'

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            PrettyPrinter(indent=4).pprint(CALC_NODES)

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

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()
        self.setWindowTitle("Calaulator Example")

        custom_stylesheet = StyleSheet.EMPTY
        custom_stylesheet.setPath("nodeeditor\\CalculatorWindow\\style\\calculator_window.qss")
        try:
            custom_stylesheet.apply(self)
        except FileNotFoundError:
            print(f"QSS file not found: {custom_stylesheet.path()}")

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

        self.actAbout = QAction(Icon(FluentIcon.HELP), "&關於", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

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
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)
    
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

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        '''設定 工具列-檔案 在無法使用時不顯示；可使用時顯示'''
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

        self.updateEditMenu()

    def updateEditMenu(self):
        '''設定 工具列-編輯 在無法使用時不顯示；可使用時顯示'''
        try:
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)
            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDeleted.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def updateWindowMenu(self):
        '''設定 工具列-視窗 在無法使用時不顯示；可使用時顯示'''
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("側面節點欄")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodeToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()
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

    def onWindowNodeToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        '''創造可移動式分割視窗'''
        self.nodeListWidget = NodeGraphicsDragListBox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodeListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.nodesDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWindClose)
        return subwnd
    
    def onSubWindClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()
    
    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)