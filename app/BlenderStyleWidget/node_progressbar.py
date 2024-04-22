from PyQt5.QtWidgets import QApplication, QProgressBar, QStyleOptionProgressBar, QStyle, QStyleOption, QWidget, QSizePolicy
from PyQt5.QtGui import QCursor, QFocusEvent, QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPointF

from common.color_sheet import color_manager
from .content_BaseSetting import ContentBaseSetting

class ControlledProgressBarStyle(QStyle, ContentBaseSetting):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionProgressBar):
                self.drawProgressBar(option, painter)

    def drawProgressBar(self, option: QStyleOptionProgressBar, painter: QPainter):
        # 繪製背景
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color_background))
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

class ControlledProgressBar(QProgressBar):
    '''
    自定義進度條
    ### Parameters:
        label (str): 進度條的標籤，預設為"Value"。
        minimum (int): 進度條的最小值，預設為0。
        maximum (int): 進度條的最大值，預設為100。
        **initial_percent (float): 進度條的初始百分比，預設為0.5。
        **tooltip (str): 自定義提示字框內容文字。

    ### Attributes:
        label (str): 進度條的標籤。
        minimum (int): 進度條的最小值。
        maximum (int): 進度條的最大值。

    ### Raises:
        ValueError: 若initial_percent不在0~1的範圍內時，會引發此錯誤。

    ### Usage:
        progressBar = ControlledProgressBar(label="Progress", minimum=0, maximum=10, initial_percent=0.8)
    '''
    def __init__(self, label="Value", minimum=0, maximum=100, parent=None, **kwargs):
        super().__init__(parent)
        height = kwargs.get("height", 23)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        initial_percent = kwargs.get("initial_percent", 0.5)

        self.label = label
        self.setRange(minimum, maximum)

        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if not isinstance(initial_percent, float):
            raise TypeError("initial_percent must be a float")
        if initial_percent < 0 or initial_percent > 1:
            raise ValueError("initial_percent must be between 0 and 1")
        self.setValue(int(initial_percent*100))

        self.setToolTip(label) if tooltip=="" else self.setToolTip(tooltip)

        if debug: self.setStyleSheet("border: 1px solid red;")

    def setRange(self, minimum: int, maximum: int) -> None:
        '''設置進度條範圍'''
        self.min_value = minimum
        self.max_value = maximum

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
        painter.drawText(QPointF(5, self.height() / 2 + 5), self.label)

        # 繪製數值
        progress = self.value() * (self.max_value - self.min_value) / 100 + self.min_value
        text = f"{progress}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        '''滑鼠點擊時更新進度'''
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.updateProgress(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseMoveEvent(self, event):
        '''滑鼠移動時，如果正在拖動，更新進度'''
        if hasattr(self, 'dragging') and self.dragging:
            self.updateProgress(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''釋放滑鼠後，停止拖動'''
        if hasattr(self, 'dragging') and self.dragging:
            self.dragging = False
            # 將滑鼠游標恢復為默認值
            QApplication.restoreOverrideCursor()
        else:
            super().mouseReleaseEvent(event)

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