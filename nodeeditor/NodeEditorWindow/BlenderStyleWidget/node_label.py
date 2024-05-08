from PyQt5.QtWidgets import QLabel, QSizePolicy

from .content_BaseSetting import ContentBaseSetting

class Label(QLabel, ContentBaseSetting):
    ''' 自定義文字
        ### Parameters:
            parent (QWidget): 父窗口部件，預設為None。
            text (str): 顯示文字內容。
            **tooltip (str): 自定義提示字框內容文字。

        ### Attributes:
            text (str): 顯示文字內容。

        ### Usage:
            label = Label(parent, text="mylabel")
    '''
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)

        if debug: self.setStyleSheet("border: 1px solid red;")