from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor, QFont, QPainter, QPen

from common.style_sheet import StyleSheet
from .content_BaseSetting import ContentBaseSetting

CURRENT_INDEX:int = 0

class ComboBoxItemDelegate(QStyledItemDelegate, ContentBaseSetting):
    '''自定義元素樣式'''
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        option_copy = QStyleOptionViewItem(option)
        # HACK：暫定設定每個元素的高度
        option_copy.rect.setHeight(25)

        border_radius = 5
        fill_rect = option.rect.adjusted(1, 1, -1, -1)
        
        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.setBrush(QColor(self.color_GRAY_24))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(fill_rect, border_radius, border_radius)
        elif option.state & QStyle.StateFlag.State_Selected:
            painter.setBrush(QColor(self.color_clicked))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(fill_rect, border_radius, border_radius)
        else:
            painter.fillRect(option.rect, QColor(0, 0, 0, 0))

        # 繪製元素內容
        self.initStyleOption(option_copy, index)
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(option.rect.adjusted(5, 0, -5, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, index.data(Qt.ItemDataRole.DisplayRole))

class ComboBox(QComboBox, ContentBaseSetting):
    """ Custom combobox
        
        Parameters :
        ---------
            parent (QWidget): The parent widget. Default is None.

        Attributes :
        ---------
            text_label (QLabel): The label displaying the current selection text.

        Usage :
        ---------
            combo_box = ComboBox(parent)
    """
    def __init__(self, parent=None, **kwargs):
        super(ComboBox, self).__init__(parent=parent)

        self.setView(QListView())
        delegate = ComboBoxItemDelegate(self)
        self.setItemDelegate(delegate)

        self.text_label = QLabel(self)
        self.text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text_label.setStyleSheet('color: #FFFFFF;')
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 滑鼠進入和離開事件處理程序
        self.enterEvent = self.mouse_enter
        self.leaveEvent = self.mouse_leave
        self.is_mouse_over = False

        self.styles_set()

    def mouse_enter(self, event):
        self.is_mouse_over = True
        self.repaint()

    def mouse_leave(self, event):
        self.is_mouse_over = False
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        border_radius = 3
        padding = 1

        fill_color = QColor(self.color_GRAY_2a)
        if self.is_mouse_over:
            fill_color = QColor(self.color_GRAY_30)

        fill_rect = rect.adjusted(padding, padding, -padding, -padding)
        painter.fillRect(fill_rect, fill_color)

        painter.setPen(QPen(QColor(self.color_GRAY_46), 0.5))

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(fill_rect, border_radius, border_radius)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect.adjusted(0, 0, 0, -self.view().height()), 10, 10)

        current_index = self.currentIndex()
        if current_index >= 0:
            current_text = self.itemText(current_index)
            self.text_label.setText(current_text)
            self.text_label.adjustSize()
            text_label_height = self.text_label.height()
            combobox_height = self.height()
            text_label_y = int((combobox_height - text_label_height) / 2)
            self.text_label.move(5, text_label_y)

    def showPopup(self):
        '''重寫 showPopup 方法，讓下拉式選單本身具有下半部圓角效果'''
        super().showPopup()
        self.view().setStyleSheet('border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;')