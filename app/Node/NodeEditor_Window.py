from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200 ,200, 800, 600)

        self.setWindowIcon(QIcon("app\\resources\\icons\\logo.png"))
        self.setWindowTitle("Manim Node Editor")
        self.show()