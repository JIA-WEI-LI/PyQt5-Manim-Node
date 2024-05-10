from PyQt5.QtWidgets import QPushButton, QSizePolicy, QDialog, QColorDialog
from .content_BaseSetting import ContentBaseSetting
from .node_lineEdit import LineEdit
from common.style_sheet import StyleSheet

class ColorPickerButton(QPushButton, ContentBaseSetting):
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
        # 創建顏色選擇器對話框
        colorPickerDialog = ColorDialog()
        color = colorPickerDialog.exec_()
        
        if color == QDialog.Accepted:
            selected_color = colorPickerDialog.selectedColor()
            self.setStyleSheet(f"background-color: {selected_color.name()}")


class ColorDialog(QColorDialog):
    '''
    自定義的顏色選擇對話框
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet("background-color: #CCCCCC;")