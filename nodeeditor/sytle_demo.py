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

        check_box.setToolTip(CheckBox.__doc__)
        combo_box.setToolTip(ComboBox.__doc__)
        color_picker_button_1.setToolTip(ColorPickerButton.__doc__)
        color_picker_button_2.setToolTip(ColorPickerButton.__doc__)
        file_dialog_widget.setToolTip(FileDialogWidget.__doc__)
        progress_bar.setToolTip(ControlledProgressBar.__doc__)
        label.setToolTip(Label.__doc__)
        line_edit.setToolTip(LineEdit.__doc__)
        button.setToolTip(PushButton.__doc__)
        spin_box.setToolTip(SpinBox.__doc__)
        vector_spin_box.setToolTip(VectorSpinBox.__doc__)

        combo_box.addItems(["Item 1", "Item 2", "Item 3"])

        self.demoStyle("CheckBox", check_box)
        self.demoStyle("ComboBox", combo_box) 
        self.demoStyle("ColorPickerButton (True) ", color_picker_button_1)
        self.demoStyle("ColorPickerButton (False) ", color_picker_button_2)
        self.demoStyle("ControlledProgressBar", progress_bar)
        self.demoStyle("FileDialogWidget", file_dialog_widget)
        self.demoStyle("Label", label)
        self.demoStyle("LineEdit", line_edit)
        self.demoStyle("PushButton", button)
        self.demoStyle("SpinBox", spin_box)
        self.demoStyle("VectorSpinBox (3 Lists)", vector_spin_box)

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

    def demoStyle(self, label_name, widget):
        hBoxLayout = QHBoxLayout()
        label = QLabel()
        label.setText(label_name)
        label.setStyleSheet("color:#ccc;")

        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        hBoxLayout.addWidget(label, stretch=4)
        hBoxLayout.addWidget(widget, stretch=6)
        self.vBoxLayout_left.addLayout(hBoxLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    demo = StyleDemo()
    demo.show()
    sys.exit(app.exec_())
