from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class LineEdit(QWidget, ContentBaseSetting):
    ''' Custom LineEdit widget

        Parameters :
        ---------
            label_text (str): The label text of the QLineEdit widget.
            max_width (float): The maximum width of the QLineEdit widget.

        Attributes :
        ---------
            label_text (str): The label text of the QLineEdit widget.
            max_width (float): The maximum width of the QLineEdit widget.

        Usage :
        ---------
            lineEdit = LineEdit(text="MyLineEdit", max_width=100)
    '''
    def __init__(self, label_text: str="", max_width:float=100, parent=None, **kwargs):
        super(LineEdit, self).__init__(parent=parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        self.max_width = max_width
        self.label_text = label_text

        self.hLayoutBox = QHBoxLayout(self)
        self.label = QLabel()
        self.label.setText(self.label_text)
        self.lineEdit = QLineEdit()

        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.lineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if self.label_text != "": 
            self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=6)
            self.hLayoutBox.addWidget(self.lineEdit, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, stretch=4)
        else:
            self.hLayoutBox.addWidget(self.lineEdit, alignment=Qt.AlignmentFlag.AlignVCenter, stretch=1)

        if self.width() > max_width - 3: self.setFixedWidth(max_width - 3)
        self.updateLabelWidth()
        
        self.setToolTip(label_text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)
        
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