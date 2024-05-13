from PyQt5.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class CheckBox(QWidget, ContentBaseSetting):
    ''' 自定義勾選框
        ### Parameters:
            parent (QWidget): 父窗口部件，預設為None。
            text (str): 顯示勾選框右側文字內容。
            **tooltip (str): 自定義提示字框內容文字。

        ### Attributes:
            text (str): 顯示勾選框右側文字內容。

        ### Usage:
            checkbox = CheckBox(parent, text="CheckBox")
    '''
    def __init__(self, text: str="Boolean", parent=None, **kwargs):
        super(CheckBox, self).__init__(parent=parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        self.text = text
        
        self.hLayoutBox = QHBoxLayout(self)
        self.checkBox = QCheckBox()
        self.label = QLabel()
        self.label.setObjectName("nodeCheckboxLabel")
        self.label.setText(self.text)

        self.checkBox.setFixedWidth(self.content_height-3)
        self.checkBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.checkBox, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=1)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)

        if debug: self.setStyleSheet("border: 1px solid red;")