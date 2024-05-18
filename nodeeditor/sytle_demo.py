import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect

import sys
sys.path.append('c:/Users/USER/Desktop/VScode/PyQt5-Manim-Node/nodeeditor/NodeEditorWindow/BlenderStyleWidget')
from NodeEditorWindow.BlenderStyleWidget.node_checkbox import CheckBox
from NodeEditorWindow.BlenderStyleWidget.node_colorPicker import ColorPickerButton
from NodeEditorWindow.BlenderStyleWidget.node_comboBox import ComboBox
from NodeEditorWindow.BlenderStyleWidget.node_label import Label
from NodeEditorWindow.BlenderStyleWidget.node_lineEdit import LineEdit
from NodeEditorWindow.BlenderStyleWidget.node_progressbar import ControlledProgressBar
from NodeEditorWindow.BlenderStyleWidget.node_pushButton import PushButton
from NodeEditorWindow.BlenderStyleWidget.node_spinBox import SpinBox
from NodeEditorWindow.BlenderStyleWidget.node_vectorSpinBox import VectorSpinBox

class StyleDemo(QWidget):
    def __init__(self):
        super().__init__()

        # 設定主佈局
        self.vBoxLayout = QVBoxLayout()

        # 標籤
        check_box = CheckBox("CheckBox")
        combo_box = ComboBox()
        color_picker_button = ColorPickerButton(show_text=True)
        progress_bar = ControlledProgressBar("ProgressBar")
        label = Label("Label")
        line_edit = LineEdit("Line Edit")
        button = PushButton("Push Button")
        spin_box = SpinBox("SpinBox")
        vector_spin_box = VectorSpinBox(["Spinbox 1", "Spinbox 2", "Spinbox 3"])

        check_box.setToolTip(CheckBox.__doc__)
        combo_box.setToolTip(ComboBox.__doc__)
        color_picker_button.setToolTip(ColorPickerButton.__doc__)
        progress_bar.setToolTip(ControlledProgressBar.__doc__)
        label.setToolTip(Label.__doc__)
        line_edit.setToolTip(LineEdit.__doc__)
        button.setToolTip(PushButton.__doc__)
        spin_box.setToolTip(SpinBox.__doc__)
        vector_spin_box.setToolTip(VectorSpinBox.__doc__)

        combo_box.addItems(["Item 1", "Item 2", "Item 3"])

        self.demoStyle("CheckBox", check_box)
        self.demoStyle("ComboBox", combo_box) 
        self.demoStyle("ColorPickerButton", color_picker_button)  
        self.demoStyle("ControlledProgressBar", progress_bar)
        self.demoStyle("Label", label)
        self.demoStyle("LineEdit", line_edit)
        self.demoStyle("PushButton", button)
        self.demoStyle("SpinBox", spin_box)
        self.demoStyle("VectorSpinBox", vector_spin_box)

        self.setLayout(self.vBoxLayout)
        self.setWindowTitle('Node Content Widgets Demo')

        self.setStyleSheet("background-color: #222;")
        self.setFixedWidth(400)
        self.adjustSize() 

    def demoStyle(self, label_name, widget):
        hBoxLayout = QHBoxLayout()
        label = QLabel()
        label.setText(label_name)
        label.setStyleSheet("color:#ccc;")

        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        hBoxLayout.addWidget(label, stretch=4)
        hBoxLayout.addWidget(widget, stretch=6)
        self.vBoxLayout.addLayout(hBoxLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    demo = StyleDemo()
    demo.show()
    sys.exit(app.exec_())
