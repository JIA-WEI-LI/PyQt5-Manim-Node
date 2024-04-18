from PyQt5.QtWidgets import QApplication, QStyleOptionSpinBox, QStyle, QStyleOption, QWidget, QSpinBox
from PyQt5.QtGui import QCursor, QFocusEvent, QMouseEvent, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPointF

from common.color_sheet import color_manager

class SpinBoxColorSetting:
    BLENDER_BACKGROUND = color_manager.get_color("ProgressbarColor", "BLENDER_BACKGROUND")
    BLENDER_PROGRESSBAR = color_manager.get_color("ProgressbarColor", "BLENDER_PROGRESSBAR")

class SpinBoxStyle(QStyle):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionSpinBox):
                self.drawSpinBox(option, painter)

    def drawSpinBox(self, option: QStyleOptionSpinBox, painter: QPainter):
        # 繪製背景
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(SpinBoxColorSetting.BLENDER_BACKGROUND))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 3, 3)  # 5 是圓角的半徑，可以自行調整

class SpinBox(QSpinBox):
    '''
    自定義可控制數值調整器
    ### Parameters:
        label (str): 調整器的標籤，預設為"Value"。
        minimum (int): 調整器的最小值，預設為0。
        maximum (int): 調整器的最大值，預設為10^6。
        **initial (float): 調整器的初始值，預設為 1。
        **tooltip (str): 自定義提示字框內容文字。

    ### Attributes:
        label (str): 調整器的標籤。
        minimum (int): 調整器的最小值。
        maximum (int): 調整器的最大值。

    ### Raises:
        ValueError: 若initial不在範圍內時，會引發此錯誤。

    ### Usage:
        spinBox = SpinBox(label="SpinBox", minimum=0, maximum=10, initial=10)
    '''
    def __init__(self, label="Value", minimum=0, maximum=100000, parent=None, **kwargs):
        super().__init__(parent)
        tooltip = kwargs.get("tooltip", "")
        initial = kwargs.get("initial", 0.5)

        self.label = label
        self.setRange(minimum, maximum)

        self.lineEdit().setStyleSheet("color: transparent;")
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setText("")

        if not isinstance(initial, float):
            raise TypeError("initial must be a float")
        if initial < self.min_value or initial > self.max_value:
            raise ValueError("initial must be between minimum and maximum")
        self.setValue(int(initial))

        self.setToolTip(label) if tooltip=="" else self.setToolTip(tooltip)

    def setRange(self, minimum: int, maximum: int) -> None:
        '''設置進度條範圍'''
        self.min_value = minimum
        self.max_value = maximum

    def paintEvent(self, event):
        painter = QPainter(self)
        style = SpinBoxStyle()
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
        progress = self.value()
        text = f"{progress}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        '''滑鼠點擊時更新進度'''
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.dragging = True
            self.last_x = event.x()
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseMoveEvent(self, event):
        '''滑鼠移動時，如果正在拖動，更新進度'''
        if hasattr(self, 'dragging') and self.dragging:
            current_x = event.x()
            total_width = self.width()
            
            # 計算滑鼠水平移動距離
            delta_x = current_x - self.last_x
            self.last_x = current_x
            
            # 根據移動距離更新 spin_percent
            spin_percent = self.value() + delta_x / total_width * 100
            if spin_percent < self.min_value:
                spin_percent = self.min_value
            if spin_percent > self.max_value:
                spin_percent = self.max_value
            
            self.setValue(int(spin_percent))
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''釋放滑鼠後，停止拖動'''
        if hasattr(self, 'dragging') and self.dragging:
            self.dragging = False
            # 將滑鼠游標恢復為默認值
            QApplication.restoreOverrideCursor()
        else:
            super().mouseReleaseEvent(event)

    def updateSpin(self, event):
        mouse_x = event.x()
        total_width = self.width()

        spin_percent = mouse_x / total_width
        if spin_percent < self.min_value:
            self.setValue(self.min_value)
            return
        if spin_percent > self.max_value:
            self.setValue(self.max_value)
            return

        # 設置實際的值
        self.setValue(int(spin_percent))