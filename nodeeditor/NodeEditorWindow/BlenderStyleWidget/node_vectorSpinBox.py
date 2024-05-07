from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

from .content_BaseSetting import ContentBaseSetting
from .node_spinBox import SpinBox

class VectorSpinBox(QWidget, ContentBaseSetting):
    def __init__(self, degree:int=3, parent=None, **kwargs):
        # TODO: 改成輸入 List[str] 並透過 List 計算維度
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        spinBox_list = [None] * degree

        self.vBoxLayout = QVBoxLayout(self)
        self.setFixedHeight((self.content_height+3)*degree)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        for deg in range(degree):
            spinBox_list[deg] = SpinBox(f"{deg}", **kwargs)
            spinBox_list[deg].setFixedHeight(27)
            self.vBoxLayout.addWidget(spinBox_list[deg])
        self.setLayout(self.vBoxLayout)

        self.setToolTip("") if tooltip=="" else self.setToolTip(tooltip)
        
        if debug: self.setStyleSheet("border: 1px solid red;")