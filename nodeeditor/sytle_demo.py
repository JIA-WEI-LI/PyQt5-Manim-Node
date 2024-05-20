import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QRect, Qt

from NodeEditorWindow.BlenderStyleWidget import *

class StyleDemo(QWidget):
    def __init__(self):
        super().__init__()

        # 設定主佈局
        # groupbox = QGroupBox()
        self.hBoxLayout = QHBoxLayout()
        self.vBoxLayout_left = QVBoxLayout()
        self.vBoxLayout_right = QVBoxLayout()

        # left vBoxLayout widdget
        check_box = CheckBox("CheckBox")
        combo_box = ComboBox()
        color_picker_button_1 = ColorPickerButton(show_text=True)
        color_picker_button_2 = ColorPickerButton(show_text=False)
        progress_bar = ControlledProgressBar("ProgressBar")
        file_dialog_widget = FileDialogWidget()
        label = Label("Label")
        line_edit = LineEdit("Line Edit")
        button = PushButton(text="Push Button")
        spin_box = SpinBox("SpinBox")
        vector_spin_box = VectorSpinBox(["Spinbox 1", "Spinbox 2", "Spinbox 3"])
        combo_box.addItems(["Item 1", "Item 2", "Item 3"])

        self.demoStyle("CheckBox", check_box, CheckBox)
        self.demoStyle("ComboBox", combo_box, ComboBox) 
        self.demoStyle("ColorPickerButton (True) ", color_picker_button_1, ColorPickerButton)
        self.demoStyle("ColorPickerButton (False) ", color_picker_button_2, ColorPickerButton)
        self.demoStyle("ControlledProgressBar", progress_bar, ControlledProgressBar)
        self.demoStyle("FileDialogWidget", file_dialog_widget, FileDialogWidget)
        self.demoStyle("Label", label, Label)
        self.demoStyle("LineEdit", line_edit,LineEdit)
        self.demoStyle("PushButton", button, PushButton)
        self.demoStyle("SpinBox", spin_box,SpinBox)
        self.demoStyle("VectorSpinBox (3 Lists)", vector_spin_box, VectorSpinBox)

        # right vBoxLayout widget
        graphics_scene = QGraphicsScene()
        graphics_view = QGraphicsView(graphics_scene)
        graphics_scene.setSceneRect(0, 0, 300, 300)
        img = QPixmap('nodeeditor\\resources\\screenshot\\20240517.png')
        pixmap_item = QGraphicsPixmapItem(img)
        graphics_scene.addItem(pixmap_item)
        graphics_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        graphics_view.fitInView(pixmap_item, Qt.KeepAspectRatio)

        self.vBoxLayout_right.addWidget(graphics_view)

        self.hBoxLayout.addLayout(self.vBoxLayout_left)
        self.hBoxLayout.addLayout(self.vBoxLayout_right)
        self.setLayout(self.hBoxLayout)
        self.setWindowTitle('Node Content Widgets Demo')

        self.setStyleSheet("background-color: #333;")
        self.setFixedWidth(800)
        self.adjustSize() 

    def demoStyle(self, label_name:str, widget:QWidget, classMethod:classmethod):
        hBoxLayout = QHBoxLayout()
        label = QLabel()
        label.setText(label_name)
        label.setStyleSheet("color:#ccc;")
        widget.setToolTip(classMethod.__doc__)

        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        hBoxLayout.addWidget(label, stretch=4)
        hBoxLayout.addWidget(widget, stretch=6)
        self.vBoxLayout_left.addLayout(hBoxLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    demo = StyleDemo()
    demo.show()
    sys.exit(app.exec_())
