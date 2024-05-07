from PyQt5.QtWidgets import QVBoxLayout, QApplication, QStyleOptionSpinBox, QStyle, QStyleOption, QWidget, QSpinBox, QSizePolicy
from PyQt5.QtGui import QCursor, QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QEvent

from .content_BaseSetting import ContentBaseSetting
from .node_spinBox import SpinBox

class Vector2SpinBox(QWidget, ContentBaseSetting):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.vBoxLayout = QVBoxLayout()
        self.xSpinBox = SpinBox("X", **kwargs)
        self.ySpinBox = SpinBox("Y", **kwargs)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.xSpinBox)
        self.vBoxLayout.addWidget(self.ySpinBox)

        self.setToolTip("") if tooltip=="" else self.setToolTip(tooltip)
        
        if debug: self.setStyleSheet("border: 1px solid red;")