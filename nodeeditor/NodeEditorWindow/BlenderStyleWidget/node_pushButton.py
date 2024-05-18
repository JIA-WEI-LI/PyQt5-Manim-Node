from PyQt5.QtWidgets import QPushButton, QSizePolicy

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class PushButton(QPushButton, ContentBaseSetting):
    '''自定義點擊式按鈕'''
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.styles_set()