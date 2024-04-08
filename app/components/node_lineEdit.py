from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor, QFont, QPainter, QPen

from common.style_sheet import StyleSheet

class LineEdit(QWidget):
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def __init__(self, text:str, parent=None):
        super(LineEdit, self).__init__(parent=parent)
        hLayoutBox = QHBoxLayout()
        label = QLabel()
        label.setText(text)
        lineEdit = QLineEdit()

        lineEdit.setFixedHeight(23)
        hLayoutBox.setContentsMargins(0, 0, 0, 0)
        hLayoutBox.addWidget(label, stretch=4, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hLayoutBox.addWidget(lineEdit, stretch=6, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(hLayoutBox)
