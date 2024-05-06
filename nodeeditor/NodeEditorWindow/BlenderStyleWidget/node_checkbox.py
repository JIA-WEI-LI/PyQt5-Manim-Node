from PyQt5.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QPaintEvent, QFont, QFontMetrics, QPainterPath, QPen, QColor
from PyQt5.QtCore import Qt, QRectF

from .content_BaseSetting import ContentBaseSetting

class BCheckBox(QCheckBox, ContentBaseSetting):
    '''
    繼承自 QCheckBox，仿造 Blender Node 內部樣式

    ### Attributes:
        CheckBoxData (WCheckBoxData): CheckBox 的資料類別，預設為 WCheckBoxData()。

    ### Parameters:
        CheckBoxData (WCheckBoxData): CheckBox 的資料類別，預設為 WCheckBoxData()。

    ### Usage:
        checkBox = CheckBox()
    '''
   
    def __init__(self, text:str="", **kwargs):
        super(BCheckBox, self).__init__(None)
        tooltip = kwargs.get("tooltip", "")
        
        self.isEnter = False
            
        self.labelFont = QFont("Times New Roman", 12, weight=QFont.Weight.Bold)
        self.labelFont.setWordSpacing(0)
        self.labelFont.setStyleHint(QFont.StyleHint.Monospace)
        self.labelFontMetrics = QFontMetrics(self.labelFont)
        self.setFont(self.labelFont)
        self.clicked.connect(self.update)  # 將點擊事件連接到更新函數

        self.setChecked(False)

        self.setToolTip(None) if tooltip=="" else self.setToolTip(tooltip)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)

        size = min(self.width(), self.height())
        rect = QRectF(0, 0, size, size)
        rect.moveCenter(QRectF(self.rect()).center())

        borderPath = QPainterPath()
        borderPath.addRoundedRect(rect, 30, 30, Qt.SizeMode.RelativeSize)

        if self.isChecked():
            painter.setBrush(self.color_clicked)
            painter.setPen(QPen(Qt.PenStyle.NoPen))
        elif self.isEnter and not self.isChecked():
            painter.setBrush(self.color_GRAY_65)
            painter.setPen(QPen(Qt.PenStyle.NoPen))
        else:
            painter.setBrush(self.color_GRAY_54)
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            
        painter.drawPath(borderPath)

        if self.isChecked():
            painter.setPen(QPen(Qt.GlobalColor.white, size * .125, cap=Qt.PenCapStyle.RoundCap, join=Qt.PenJoinStyle.RoundJoin))
            arrow_path = QPainterPath()
            arrow_path.moveTo(size * .25, size * .5)
            arrow_path.lineTo(size * .40, size * .65)
            arrow_path.lineTo(size * .7, size * .325)
            painter.drawPath(arrow_path.translated(rect.topLeft()))

    def enterEvent(self, event):
        self.isEnter = True

    def leaveEvent(self, event):
        self.isEnter = False

class CheckBox(QWidget):
    def __init__(self, text: str="Boolean", parent=None, **kwargs):
        super(CheckBox, self).__init__(parent=parent)
        height = kwargs.get("height", 23)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)
        self.text = text
        
        self.hLayoutBox = QHBoxLayout(self)
        # self.checkBox = BCheckBox()
        self.checkBox = QCheckBox()
        self.label = QLabel()
        self.label.setObjectName("nodeCheckboxLabel")
        self.label.setText(self.text)

        self.checkBox.setFixedWidth(height-3)
        self.checkBox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        self.hLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.hLayoutBox.addWidget(self.checkBox, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.hLayoutBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, stretch=1)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        

        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)

        if debug: self.setStyleSheet("border: 1px solid red;")