from PyQt5.QtWidgets import QLabel, QSizePolicy

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

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.styles_set()