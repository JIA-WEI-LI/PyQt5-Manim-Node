from PyQt5.QtWidgets import QApplication, QStyleOptionSpinBox, QStyle, QStyleOption, QWidget, QSpinBox, QSizePolicy, QInputDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit
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
    """ Custom spinbox that can be control.

        Parameters :
        ---------
            label (str): The label text of the SpinBox widget.
            minimum (int): The minimum value of the SpinBox. Default is 0.
            maximum (int): The maximum value of the SpinBox. Default is 1000000.
            initial_value (Union[float, int]): The initial value of the SpinBox. Default is 1.

        Attributes:
        ---------
            label (str): The label text of the SpinBox widget.
                minimum (int): The minimum value of the SpinBox. Default is 0.
                maximum (int): The maximum value of the SpinBox. Default is 1000000.
                initial_value (Union[float, int]): The initial value of the SpinBox. Default is 1.
        
        Raises:
        ---------
            ValueError: If initial_value is not an integer.

        Usage:
        ---------
            SpinBox = SpinBox(label="SpinBox", minimum=0, maximum=100000, initial_value=1)
    """
    def __init__(self, label:str="Value", minimum:int=0, maximum:int=100000, initial_value:int=1, parent=None, **kwargs):
        super().__init__(parent)
        self.initial_value = initial_value

        self.isEnter = False
        self.dragging = False
        self.label = label
        self.setRange(minimum, maximum)
        
        self.lineEdit().setVisible(False)
        self.lineEdit().setDisabled(True)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._setInitialValue(self.initial_value)

        self.styles_set()

    def setRange(self, minimum: int, maximum: int) -> None:
        '''設置進度條範圍'''
        self.min_value = minimum
        self.max_value = maximum

    def _setInitialValue(self, initial_value: int):
        '''Set the initial value of the progress bar based on the input.

        The initial value can be provided as either a float representing a percentage
        (e.g., 0.5 for 50%) or an integer representing an absolute value.
        '''
        if isinstance(initial_value, int):
            self.setValue(initial_value)
        else: raise TypeError("initial_value must be an integer")

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
        painter.drawText(QPointF(10, self.height() / 2 + 5), self.label)

        # 繪製數值
        text = f"{self.initial_value}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        '''滑鼠點擊時更新進度'''
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.last_mouse_x = event.x()
            self.update()
            self.updateValue(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseMoveEvent(self, event: QMouseEvent):
        '''滑鼠移動時，如果正在拖動，更新進度'''
        if hasattr(self, 'dragging') and self.dragging:
            self.updateValue(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        '''釋放滑鼠後，停止拖動'''
        if hasattr(self, 'dragging') and self.dragging:
            self.dragging = False
            # 將滑鼠游標恢復為默認值
            QApplication.restoreOverrideCursor()
            self.update()
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.showInputDialog()

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = False
        self.update()

    def showInputDialog(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle(self.label)
        dialog.exec()

    def updateValue(self, event):
        mouse_x = event.x()
        speed = 2 if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier else 1
        # 計算實際進度值
        self.initial_value += int((mouse_x - self.last_mouse_x) / speed)
        self.last_mouse_x = event.x()
        if self.initial_value < self.min_value: self.initial_value = self.min_value
        if self.initial_value > self.max_value: self.initial_value = self.max_value

        if self.debug: print(" > min_value =", self.min_value, ", max_value = ", self.max_value, ", current = ", self.initial_value)
        # 設置SpinBox的值
        self.setValue(self.initial_value)
