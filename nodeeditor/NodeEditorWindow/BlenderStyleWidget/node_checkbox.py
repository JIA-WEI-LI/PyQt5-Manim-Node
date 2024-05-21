from PyQt5.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

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
    def __init__(self, text: str="Boolean", status:bool=False, parent=None, **kwargs):
        super(CheckBox, self).__init__(parent=parent)
        self.text = text
        
        self.hLayoutBox = QHBoxLayout(self)
        self.checkBox = QCheckBox()
        self.label = QLabel()
        self.label.setObjectName("nodeCheckboxLabel")
        self.label.setText(self.text)

        self.checkBox.setFixedWidth(self.content_height-3)
        self.checkBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.checkBox.setChecked(status)

        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.checkBox, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=1)
        self.checkBox.toggled.connect(self.updateStatus)

        self.styles_set()

    def updateStatus(self):
        """Update ContentLists for serialization"""
        status = self.checkBox.isChecked()
        if hasattr(self.parent(), 'contentLists') and self.parent().contentLists is not None:
            for item in self.parent().contentLists:
                if item[0] == 'checkbox' and item[1]['text'] == self.label.text():
                    item[1]['status'] = status
                    break