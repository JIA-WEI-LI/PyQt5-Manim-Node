from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QColorDialog, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from .content_BaseSetting import ContentBaseSetting

class ColorPicker(QPushButton, ContentBaseSetting):
    '''
    自定義顏色選擇器按鈕
    ### Parameters:
        text (str): 按鈕上的文字，預設為空。
        parent (QWidget): 父窗口部件，預設為None。
        **kwargs: 其他可選參數。
            tooltip (str): 自定義提示框內容文字。
            debug (bool): 是否啟用調試模式，預設為False。
    ### Usage:
        color_picker = ColorPicker(text="選擇顏色")
    '''
    def __init__(self, text: str="", parent=None, **kwargs):
        super().__init__(text, parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.clicked.connect(self.pickColor)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)

        if debug: 
            self.setStyleSheet("border: 1px solid red;")

    def pickColor(self):
        # 顯示顏色選擇器對話框
        color = QColorDialog.getColor()

        if color.isValid():
            # 如果選擇有效的顏色，則設置按鈕背景色
            self.setStyleSheet(f"background-color: {color.name()}")
