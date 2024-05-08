from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

from .content_BaseSetting import ContentBaseSetting
from .node_spinBox import SpinBox

class VectorSpinBox(QWidget, ContentBaseSetting):
    def __init__(self, degree:list=["x", "y", "z"], parent=None, **kwargs):
        super().__init__(parent)
        # BUG: 目前此功能高度與節點高度仍有些微落差
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        spinBox_list = [None] * len(degree)

        self.vBoxLayout = QVBoxLayout(self)
        self.setFixedHeight((self.content_height+3)*len(degree))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        for deg in range(len(degree)):
            spinBox_list[deg] = SpinBox(degree[deg], **kwargs)
            spinBox_list[deg].setFixedHeight(27)
            self.vBoxLayout.addWidget(spinBox_list[deg])
        self.setLayout(self.vBoxLayout)

        self.setToolTip("") if tooltip=="" else self.setToolTip(tooltip)
        
        if debug: self.setStyleSheet("border: 1px solid red;")