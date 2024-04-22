from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet

class LineEdit(QWidget):
    '''
        自定義LineEdit部件
        ### Parameters:
            text (str): QLineEdit部件的標籤文字。
            max_width (float): QLineEdit部件的最大寬度。
            **tooltip (str): 自定義提示字框內容文字。

        ### Attributes:
            text (str): QLineEdit部件的標籤文字。
            max_width (float): QLineEdit部件的最大寬度。

        ### Usage:
            lineEdit = LineEdit(text="MyLineEdit", max_width=100)
    '''
    def __init__(self, text: str, max_width:float, parent=None, **kwargs):
        super(LineEdit, self).__init__(parent=parent)
        height = kwargs.get("height", 23)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        self.max_width = max_width
        self.text = text

        self.hLayoutBox = QHBoxLayout(self)
        self.label = QLabel()
        self.label.setText(self.text)
        self.lineEdit = QLineEdit()

        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=6)
        self.hLayoutBox.addWidget(self.lineEdit, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, stretch=4)

        if self.width() > max_width - 3: self.setFixedWidth(max_width - 3)
        self.updateLabelWidth()
        
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        
        if debug: self.setStyleSheet("border: 1px solid red;")

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget.setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget.setEditingFlag(False)
        super().focusOutEvent(event)

    def resizeEvent(self, event):
        super(LineEdit, self).resizeEvent(event)
        self.updateLabelWidth()

    def updateLabelWidth(self):
        max_width = 0.6 * self.width()  # 限制為 Layout 寬度的 60%
        label_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        if label_width > max_width:
            self.label.setText(self.label.text()[:int(max_width / label_width * len(self.label.text())) - 3] + '...')