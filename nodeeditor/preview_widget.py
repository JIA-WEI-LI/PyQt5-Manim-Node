from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy

from BlenderStyleWidget import *
from common.style_sheet import StyleSheet

class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview Window")
        self.initUI()

    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def initUI(self):
        vBoxLayout = QVBoxLayout()
        hBoxLayout = QHBoxLayout()
        layout = QHBoxLayout()

        main_title = QLabel()
        main_title.setText("預覽元件")
        # 添加示例元件
        button1 = PushButton("Button 1")
        checkbox = CheckBox("checkbox 2")

        vBoxLayout.addWidget(main_title)
        layout.addWidget(button1)
        layout.addWidget(checkbox)
        vBoxLayout.addLayout(layout)

        self.setLayout(vBoxLayout)

        self.setGeometry(200 ,200, 800, 600)
        self.setWindowTitle("Manim Node Editor -- Content Preview")
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    preview_window = PreviewWindow()
    preview_window.show()
    app.exec_()
