from PyQt5.QtCore import Qt, QSignalMapper
from PyQt5.QtWidgets import QMainWindow, QWidget, QMdiArea, QListWidget, QDockWidget, QAction, QMessageBox
from PyQt5.QtGui import QCloseEvent, QKeySequence

from common.utils import dumpException
from NodeEditorWindow import NodeEditorMainWindow

class CalaulatorMainWindow(NodeEditorMainWindow):
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

    def updateMenus(self):
        pass

    def createActions(self):
        super().createActions()

        self.closeAct = QAction("&關閉子視窗", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.closeAllAct = QAction("關閉&全視窗", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.tileAct = QAction("&磚瓦式分割", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.cascadeAct = QAction("&瀑布式分割", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.nextAct = QAction("&下一視窗", self, shortcut=QKeySequence.StandardKey.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.previousAct = QAction("&上一視窗", self, shortcut=QKeySequence.StandardKey.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)
        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&關於", self, statusTip="Show the application's About box", triggered=self.about)
    
    def about(self):
        QMessageBox.about(self, "關於計算器節點編輯器範例",
                          "此 <b>計算器節點編輯器</b> 範例在於如何使用雙介面演示 PyQt5 和 節點編輯器，相關訊息可以參閱： "
                          "<a href='https://github.com/JIA-WEI-LI/PyQt5-Manim-Node'>Manim Community 節點編輯器</a>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&視窗")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu('&幫助')
        self.helpMenu.addAction(self.aboutAct)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows)!=0)

        # for i, window in enumerate(windows):
        #     child = window.widget()

        #     text = "%d %s" % (i+1, child.userFriendlyCurrentFile())
        #     if i<9:
        #         text = '&' + text

        #     action = self.windowMenu.addAction(text)
        #     action.setCheckable(True)
        #     action.setChecked(child in self.activeMdiChild())
        #     action.triggered.connect(self.windowMapper.map)
        #     self.windowMapper.setMapping(action, window)

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

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.items)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)