from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon

from config.icon import Icon

class NodeEditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200 ,200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # 創建圖像場景
        self.graphicsScene = QGraphicsScene()

        # 創建圖像視圖
        self.view = QGraphicsView(self)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)

        self.setWindowIcon(QIcon(Icon.WINDOW_LOGO))
        self.setWindowTitle("Manim Node Editor")
        self.show()