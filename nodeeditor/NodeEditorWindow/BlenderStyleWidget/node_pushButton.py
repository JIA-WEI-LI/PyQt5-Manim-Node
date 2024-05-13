from PyQt5.QtWidgets import QPushButton, QSizePolicy

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class PushButton(QPushButton, ContentBaseSetting):
    '''自定義點擊式按鈕'''
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)
        
        if debug: self.setStyleSheet("border: 1px solid red;")