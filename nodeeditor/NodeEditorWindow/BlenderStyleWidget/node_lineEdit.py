from PyQt5.QtGui import QFocusEvent, QPaintEvent, QPainter, QColor, QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QStyle, QLineEdit, QSizePolicy, QStyleOption, QStyleOptionFrame
from PyQt5.QtCore import Qt, QEvent

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

class LineEditStyle(QStyle, ContentBaseSetting):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        self.widget = widget
        if isinstance(option, QStyleOptionFrame):
            self.drawLineEdit(option, painter)

    # def drawPrimitive(self, element: QStyle.PrimitiveElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
    #     self.widget = widget
    #     if element == QStyle.PrimitiveElement.PE_PanelLineEdit:
    #         if isinstance(option, QStyleOptionFrame):
    #             self.drawLineEdit(option, painter)

    def drawLineEdit(self, option: QStyleOptionFrame, painter: QPainter):
        # 繪製背景
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 隨滑鼠動作改變顏色
        if getattr(self.widget, 'isEnter', False) and getattr(self.widget, 'dragging', False):
            painter.setBrush(QColor(self.color_mouseover))
        elif getattr(self.widget, 'isEnter', False) and not getattr(self.widget, 'dragging', False):
            painter.setBrush(QColor(self.color_GRAY_65))
        else:
            painter.setBrush(QColor(self.color_GRAY_54))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 3, 3)  # 3 是圓角的半徑，可以自行調整

class LineEdit(QLineEdit, ContentBaseSetting):
    ''' Custom LineEdit widget

        Parameters :
        ---------
            label_text (str): The label text of the QLineEdit widget.

        Attributes :
        ---------
            label_text (str): The label text of the QLineEdit widget.

        Usage :
        ---------
            lineEdit = LineEdit(text="MyLineEdit")
    '''
    def __init__(self, text:str="", parent=None, **kwargs):
        super(LineEdit, self).__init__(parent=parent)
        tooltip = kwargs.get("tooltip", "")
        self.debug = kwargs.get("debug", False)
        self.lineEdit = QLineEdit()
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)

        if self.debug: self.setStyleSheet("border: 1px solid red;")

    def paintEvent(self, event):
        painter = QPainter(self)
        style = LineEditStyle()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionFrame()
        opt.rect = self.rect().adjusted(1, 1, -1, -1)
        style.drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter, self)
        painter.end()
        super(LineEdit, self).paintEvent(event)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QEvent.Enter:
                self.isEnter = True
                self.update()
            elif event.type() == QEvent.Leave:
                self.isEnter = False
                self.update()
            elif event.type() == QEvent.MouseButtonPress:
                self.dragging = True
                self.update()
            elif event.type() == QEvent.MouseButtonRelease:
                self.dragging = False
                self.update()
        return super().eventFilter(obj, event)