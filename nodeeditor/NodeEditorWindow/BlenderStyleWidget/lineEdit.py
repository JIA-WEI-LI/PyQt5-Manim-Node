from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout

from common.style_sheet import BlenderStyleSheet
from .content_BaseSetting import ContentBaseSetting

class LineEdit(QLineEdit, ContentBaseSetting):
    """
    This is a custom QLineEdit with additional features such as focus policies, hover and press states, 
    and custom key press handling.

    Parameters
    -----------
    parent : QWidget, optional

        The parent widget of the line edit. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QLineEdit constructor.

    Examples
    --------
    
    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from wblenderstylewidget import LineEdit

        app = QApplication([])
        window = QMainWindow()
        line_edit = LineEdit()
        window.setCentralWidget(line_edit)
        window.show()
        app.exec_()
    """
    def __init__(self, place_holder:str="", parent=None, **kwargs):
        super(LineEdit, self).__init__(parent=parent)
        self.setObjectName("LineEdit")
        self.setPlaceholderText(place_holder)
        self.BaseSetting()
        self.innerSetting()
        BlenderStyleSheet.LINEEDIT.apply(self)
        
    def innerSetting(self):
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def mousePressEvent(self, event: QMouseEvent):
        self.isPressed = True
        self.editing = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.isPressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event: QMouseEvent):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event: QMouseEvent):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if self.editing:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape):
                self.clearFocus()
        super().keyPressEvent(event)