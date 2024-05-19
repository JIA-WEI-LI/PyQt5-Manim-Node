from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

class NodeGraphicsDragListBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragDropMode(True)

        self.addMyItems()

    def addMyItems(self):
        self.addMyItem("Input", "nodeeditor\\resources\\icons\\icon_check.svg")
        self.addMyItem("Input", "nodeeditor\\resources\\icons\\icon_check.svg")
        self.addMyItem("Input", "nodeeditor\\resources\\icons\\icon_check.svg")
        self.addMyItem("Input", "nodeeditor\\resources\\icons\\icon_check.svg")
        self.addMyItem("Input", "nodeeditor\\resources\\icons\\icon_check.svg")
        
    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)
        pixamp = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixamp))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled)

        item.setData(Qt.UserRole, pixamp)
        item.setData(Qt.UserRole + 1, op_code)