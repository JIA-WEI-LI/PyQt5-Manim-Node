from PyQt5.QtWidgets import QWidget

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200 ,200, 800, 600)

        self.setWindowTitle("Manim Node Editor")
        self.show()