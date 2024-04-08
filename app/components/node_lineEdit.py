from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet

class LineEdit(QWidget):
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def __init__(self, text: str, max_width:float,parent=None):
        super(LineEdit, self).__init__(parent=parent)
        self.max_width = max_width

        self.hLayoutBox = QHBoxLayout(self)
        self.label = QLabel()
        self.label.setText(text)
        self.lineEdit = QLineEdit()

        self.lineEdit.setFixedHeight(23)
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=6)
        self.hLayoutBox.addWidget(self.lineEdit, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, stretch=4)

        if self.width() > max_width - 3: self.setFixedWidth(max_width - 3)
        self.updateLabelWidth()

        self.setToolTip(text)

    def resizeEvent(self, event):
        super(LineEdit, self).resizeEvent(event)
        self.updateLabelWidth()

    def updateLabelWidth(self):
        max_width = 0.6 * self.width()  # 限制為 Layout 寬度的 60%
        label_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        if label_width > max_width:
            self.label.setText(self.label.text()[:int(max_width / label_width * len(self.label.text())) - 3] + '...')