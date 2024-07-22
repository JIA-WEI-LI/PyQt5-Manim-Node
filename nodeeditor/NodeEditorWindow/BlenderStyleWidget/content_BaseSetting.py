from PyQt5.QtWidgets import QSizePolicy, QWidget
from PyQt5.QtGui import QFont

from common.style_sheet import StyleSheet

class ContentBaseSetting:
    FONT = QFont("Sans Mono", 11)

    def __init__(self, apply_style=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tooltip = kwargs.get("tooltip", "")
        self.debug = kwargs.get("debug", False)
        self.content_height = kwargs.get("content_height", 24)

    def styles_set(self):
        self.setToolTip(self.tooltip)
        StyleSheet.applyStyle("node_content", self)
        if self.debug: self.setStyleSheet("border: 1px solid red;")

    def BaseSetting(self):
        self.isPressed = False
        self.isHover = False

        self.setFont(self.FONT)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # if hasattr(BlenderStyleSheet, self.__class__.__name__.upper()):
        #     getattr(BlenderStyleSheet, self.__class__.__name__.upper()).apply(self)

    def setFixedHeight(self, height):
        default_height = 30
        new_height = height if height is not None else default_height
        super().setFixedHeight(new_height)