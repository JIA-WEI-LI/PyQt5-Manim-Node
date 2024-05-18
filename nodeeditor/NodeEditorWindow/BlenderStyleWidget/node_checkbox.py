from PyQt5.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class CheckBox(QWidget, ContentBaseSetting):
    """ Custom Checkbox

        Parameters:
        ---------
            text (str): The text displayed on the right side of the checkbox.
        
        Attributes:
        ---------
            text (str): The text displayed on the right side of the checkbox.

        Usage:
        ---------
            checkbox = CheckBox(parent, text="Checkbox")
    """
    def __init__(self, text: str="Boolean", parent=None, **kwargs):
        super(CheckBox, self).__init__(parent=parent)
        self.text = text
        
        self.hLayoutBox = QHBoxLayout(self)
        self.checkBox = QCheckBox()
        self.label = QLabel()
        self.label.setObjectName("nodeCheckboxLabel")
        self.label.setText(self.text)

        self.checkBox.setFixedWidth(self.content_height-3)
        self.checkBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.checkBox, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=1)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.styles_set()