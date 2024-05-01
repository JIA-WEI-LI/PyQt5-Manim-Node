from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy

from common.style_sheet import StyleSheet

class Label(QLabel):
    '''自定義文字'''
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)
        height = kwargs.get("height", 23)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)

        if debug: self.setStyleSheet("border: 1px solid red;")