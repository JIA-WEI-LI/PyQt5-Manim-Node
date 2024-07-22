from PyQt5.QtCore import QSize, Qt, QByteArray, QDataStream, QIODevice, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QDrag
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

from common import *

from .calculator_config import *

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
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:
            node = get_class_from_opcode(key)
            self.addMyItem(node.op_title, node.icon, node.op_code)
        
    def addMyItem(self, name, icon=Icon(FluentIcon.CLOSE), op_code=0):
        item = QListWidgetItem(name, self)
        item.setIcon(icon)
        item.setSizeHint(QSize(32, 32))
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            # print("dragging item <%d>" % op_code, item)

            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(int(pixmap.width()/2), int(pixmap.height()/2)))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: dumpException(e)