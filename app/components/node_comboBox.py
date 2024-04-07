from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPen

class CustomItemDelegate(QStyledItemDelegate):
    '''自定義元素樣式'''
    def paint(self, painter, option, index):
        option_copy = QStyleOptionViewItem(option)
        # 設定每個元素的高度
        option_copy.rect.setHeight(25)
        
        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, QColor('#464646'))
        elif option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor('#4772b3'))
        else:
            painter.fillRect(option.rect, QColor('#181818'))

        # 繪製元素內容
        self.initStyleOption(option_copy, index)
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(option.rect.adjusted(5, 0, -5, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, index.data(Qt.ItemDataRole.DisplayRole))

class ComboBox(QComboBox):
    '''自定義下拉式選單'''
    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent=parent)
        self.setView(QListView())
        delegate = CustomItemDelegate(self)
        self.setItemDelegate(delegate)

        self.text_label = QLabel(self)
        self.text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text_label.setStyleSheet('color: #FFFFFF;')

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        border_radius = 3
        padding = 1

        fill_rect = rect.adjusted(padding, padding, -padding, -padding)
        painter.fillRect(fill_rect, QColor('#242424'))

        painter.setPen(QPen(QColor('#464646'), 0.5))

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(fill_rect, border_radius, border_radius)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect.adjusted(0, 0, 0, -self.view().height()), 10, 10)

        current_index = self.currentIndex()
        if current_index >= 0:
            current_text = self.itemText(current_index)
            self.text_label.setText(current_text)
            # 在設置完文本後，重新計算 text_label 的大小
            self.text_label.adjustSize()
            # 計算 text_label 的位置，使其置中於 ComboBox 的高度
            text_label_height = self.text_label.height()
            combobox_height = self.height()
            text_label_y = int((combobox_height - text_label_height) / 2)
            self.text_label.move(5, text_label_y)

# 使用方法
# custom_combo_box = CustomComboBox(parent)
