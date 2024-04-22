from PyQt5.QtWidgets import QApplication, QPushButton, QSizePolicy

from common.style_sheet import StyleSheet

class PushButton(QPushButton):
    '''自定義點擊式按鈕'''
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)
        height = kwargs.get("height", 22)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)

        if debug: self.setStyleSheet("border: 1px solid red;")