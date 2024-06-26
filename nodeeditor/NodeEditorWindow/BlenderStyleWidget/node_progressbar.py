from typing import Union
from PyQt5.QtWidgets import QApplication, QProgressBar, QStyleOptionProgressBar, QStyle, QStyleOption, QWidget, QSizePolicy
from PyQt5.QtGui import QCursor, QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import QEvent, Qt, QPointF

from .content_BaseSetting import ContentBaseSetting

class ControlledProgressBarStyle(QStyle, ContentBaseSetting):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        self.widget = widget
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionProgressBar):
                self.drawProgressBar(option, painter)

    def drawProgressBar(self, option: QStyleOptionProgressBar, painter: QPainter):
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 隨滑鼠動作改變顏色
        if self.widget.isEnter and self.widget.dragging:
            painter.setBrush(QColor(self.color_mouseover))
        elif self.widget.isEnter and not self.widget.dragging:
            painter.setBrush(QColor(self.color_GRAY_65))
        else:
            painter.setBrush(QColor(self.color_GRAY_54))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 3, 3)  # 5 是圓角的半徑，可以自行調整

        # 繪製進度條（帶有圓角效果）
        progress_rect = background_rect.adjusted(0, 0, 0, 0)
        progress_width = int(progress_rect.width() * (option.progress / 100.0))
        progress_rect.setWidth(progress_width)

        # 繪製帶有圓角效果的進度條
        progress_color = QColor(self.color_clicked)
        painter.setBrush(progress_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(progress_rect, 3, 3)

class ControlledProgressBar(QProgressBar, ContentBaseSetting):
    """ Custom progress bar that can be control.

        Parameters :
        ---------
            label (str): The label text of the ProgressBar widget.
            minimum (int): The minimum value of the ProgressBar. Default is 0.
            maximum (int): The maximum value of the ProgressBar. Default is 100.
            initial_value (Union[float, int]): The initial value of the ProgressBar. Default is 0.5.

        Attributes:
        ---------
            label (str): The label text of the ProgressBar widget.
            minimum (int): The minimum value of the ProgressBar. Default is 0.
            maximum (int): The maximum value of the ProgressBar. Default is 100.
            initial_value (Union[float, int]): The initial value of the ProgressBar. Default is 0.5.
        
        Raises:
        ---------
            ValueError: If initial_value is not a float or an integer.

        Usage:
        ---------
            progressBar = ControlledProgressBar(label="Progress", minimum=0, maximum=100, initial_value=0.5)
    """
    def __init__(self, label="Value", minimum:int=0, maximum:int=100 , initial_value: Union[float, int]=0.5, parent=None, **kwargs):
        super().__init__(parent)
        self.initial_value = initial_value
        self.apply_style = False

        self.isEnter = False
        self.dragging = False
        self.label = label
        self.setRange(minimum, maximum)

        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._setInitialValue(self.initial_value)
        self.valueChanged.connect(self.updateContentList)
        self.styles_set()

    def setRange(self, minimum: int, maximum: int) -> None:
        self.min_value = minimum
        self.max_value = maximum

    def _setInitialValue(self, initial_value: Union[float, int]):
        '''Set the initial value of the progress bar based on the input.

        The initial value can be provided as either a float representing a percentage
        (e.g., 0.5 for 50%) or an integer representing an absolute value.
        '''
        if isinstance(initial_value, float) and 0 <= initial_value <= 1:
            self.setValue(int(initial_value * 100))
        elif isinstance(initial_value, int) or isinstance(initial_value, float):
            self.setValue(initial_value)
        else: raise TypeError("initial_value must be a float or an integer")

    def paintEvent(self, event):
        painter = QPainter(self)
        style = ControlledProgressBarStyle()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionProgressBar()
        self.initStyleOption(opt)
        opt.rect = self.rect().adjusted(1, 1, -1, -1)
        opt.textVisible = self.isTextVisible()

        style.drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter, self)

        # 繪製文字
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(QPointF(10, self.height() / 2 + 5), self.label)

        # 繪製數值
        progress = self.value() * (self.max_value - self.min_value) / 100 + self.min_value
        text = f"{progress}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.update()
            self.updateProgress(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        return super().mouseDoubleClickEvent(event)
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragging') and self.dragging:
            self.updateProgress(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
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

    def updateProgress(self, event):
        mouse_x = event.x()
        total_width = self.width()

        progress_percent = mouse_x / total_width
        if progress_percent < 0:
            self.setValue(0)
            return
        if progress_percent > 1:
            self.setValue(100)
            return
        # 計算實際進度值
        value = progress_percent * (self.max_value - self.min_value) + self.min_value

        # 設置進度條的值
        self.setValue(int(progress_percent * 100))

    def updateContentList(self):
        '''Update ContentLists for serialization'''
        progress_value = self.value()
        if hasattr(self.parent(), 'contentLists') and self.parent().contentLists is not None:
            for item in self.parent().contentLists:
                if item[0] == 'progressBar' and item[1]['label'] == self.label:
                    item[1]['initial_value'] = progress_value
                    break