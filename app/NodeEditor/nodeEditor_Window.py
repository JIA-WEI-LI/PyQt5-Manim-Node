from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QIcon

from config.icon import Icon
from .nodeEditor_Widget import NodeEditorWidget

class NodeEditorWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')

        nodeEditor = NodeEditorWidget(self)
        self.setCentralWidget(nodeEditor)

        self.setGeometry(200 ,200, 800, 600)
        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()