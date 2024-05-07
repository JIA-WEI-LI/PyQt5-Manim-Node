from PyQt5.QtWidgets import QApplication, QStyleOptionSpinBox, QStyle, QStyleOption, QWidget, QSpinBox, QSizePolicy
from PyQt5.QtGui import QCursor, QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QEvent

from .content_BaseSetting import ContentBaseSetting

class SpinBoxStyle(QStyle, ContentBaseSetting):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        self.widget = widget
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionSpinBox):
                self.drawSpinBox(option, painter)
        elif element == QStyle.ControlElement.CE_SpinBox:
            self.drawSpinBoxButtons(option, painter)
            self.drawSpinBox(option, painter)  # 繪製SpinBox背景

    def drawSpinBox(self, option: QStyleOptionSpinBox, painter: QPainter):
        # 繪製背景
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 根據滑鼠動作改變顏色
        if self.widget.isEnter and self.widget.dragging:
            painter.setBrush(QColor(self.color_GRAY_65))
        elif self.widget.isEnter and not self.widget.dragging:
            painter.setBrush(QColor(self.color_GRAY_65))
        else:
            painter.setBrush(QColor(self.color_GRAY_54))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 3, 3)# 5 是圓角的半徑，可以自行調整

    def drawSpinBoxButtons(self, option: QStyleOption, painter: QPainter):
        if option.subControls & QStyle.SubControl.SC_SpinBoxUp:
            self.drawSpinBoxButton(QStyleOptionSpinBox.subControls.SC_SpinBoxUp, option, painter)
        if option.subControls & QStyle.SubControl.SC_SpinBoxDown:
            self.drawSpinBoxButton(QStyleOptionSpinBox.subControls.SC_SpinBoxDown, option, painter)

    def drawSpinBoxButton(self, button: QStyleOptionSpinBox, option: QStyleOption, painter: QPainter):
        button_rect = self.subControlRect(QStyle.ComplexControl.CC_SpinBox, option, button)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color_GRAY_54))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(button_rect, 3, 3)

class SpinBox(QSpinBox, ContentBaseSetting):
    '''
    自定義SpinBox
    ### Parameters:
        label (str): SpinBox的標籤，預設為"Value"。
        minimum (int): SpinBox的最小值，預設為0。
        maximum (int): SpinBox的最大值，預設為100。
        **initial_percent (float): SpinBox的初始百分比，預設為0.5。
        **tooltip (str): 自定義提示字框內容文字。

    ### Attributes:
        label (str): SpinBox的標籤。
        minimum (int): SpinBox的最小值。
        maximum (int): SpinBox的最大值。

    ### Raises:
        ValueError: 若initial_percent不在0~1的範圍內時，會引發此錯誤。

    ### Usage:
        spinBox = ControlledSpinBox(label="Value", minimum=0, maximum=10, initial_percent=0.8)
    '''
    def __init__(self, label="Value", minimum=0, maximum=100000, parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        self.debug = kwargs.get("debug", False)
        self.current_value = kwargs.get("value", 1)

        self.isEnter = False
        self.dragging = False
        self.label = label
        self.setRange(minimum, maximum)
        
        self.lineEdit().setVisible(False)
        self.lineEdit().setDisabled(True)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # if not isinstance(value, int):
        #     raise TypeError("initial_percent must be a int")
        self.setValue(int(self.current_value))

        self.setToolTip(label) if tooltip=="" else self.setToolTip(tooltip)

        if self.debug: self.setStyleSheet("border: 1px solid red;")

    def setRange(self, minimum: int, maximum: int) -> None:
        '''設置進度條範圍'''
        self.min_value = minimum
        self.max_value = maximum

    def paintEvent(self, event):
        painter = QPainter(self)
        style = SpinBoxStyle()  # 使用您定義的SpinBoxStyle
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionSpinBox()
        self.initStyleOption(opt)
        opt.rect = self.rect().adjusted(1, 1, -1, -1)

        style.drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter, self)

        # 繪製文字
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(QPointF(5, self.height() / 2 + 5), self.label)

        # 繪製數值
        text = f"{self.current_value}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def mousePressEvent(self, event):
        '''滑鼠點擊時更新進度'''
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.last_mouse_x = event.x()
            self.update()
            self.updateValue(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseMoveEvent(self, event):
        '''滑鼠移動時，如果正在拖動，更新進度'''
        if hasattr(self, 'dragging') and self.dragging:
            self.updateValue(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''釋放滑鼠後，停止拖動'''
        if hasattr(self, 'dragging') and self.dragging:
            self.dragging = False
            # 將滑鼠游標恢復為默認值
            QApplication.restoreOverrideCursor()
            self.update()
        else:
            super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = False
        self.update()

    def updateValue(self, event):
        mouse_x = event.x()
        # 計算實際進度值
        self.current_value += int(mouse_x - self.last_mouse_x)
        if self.current_value < self.min_value: self.current_value = self.min_value
        if self.current_value > self.max_value: self.current_value = self.max_value

        if self.debug: print(" > min_value =", self.min_value, ", max_value = ", self.max_value, ", current = ", self.current_value)
        # 設置SpinBox的值
        self.setValue(self.current_value)
