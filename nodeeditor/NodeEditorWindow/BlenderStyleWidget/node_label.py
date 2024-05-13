from PyQt5.QtWidgets import QLabel, QSizePolicy

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class Label(QLabel, ContentBaseSetting):
    """ Custom label
        Parameters :
        ---------
            text (str): The text displayed on the label.
            parent (QWidget): The parent widget. Default is None.
            

        Attributes :
        ---------
            text_label (QLabel): The label displaying the current selection text.

        Usage :
        ---------
            label = Label(text="Label Text")
    """
    def __init__(self, text:str="", parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)

        if debug: self.setStyleSheet("border: 1px solid red;")