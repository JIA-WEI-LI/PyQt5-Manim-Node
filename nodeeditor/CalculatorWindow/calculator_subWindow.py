from PyQt5.QtCore import Qt, QDataStream, QIODevice
from PyQt5.QtGui import QDragEnterEvent, QPixmap

from NodeEditorWindow.nodeEditor_Widget import NodeEditorWidget
from NodeEditorNodes.node_Calculator import *

from common.utils import dumpException
from .calculator_config import *

class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterlisteners(self.onDragEnter)
        self.scene.addDropListeners(self.onDrop)

        self._close_event_listeners = []

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event: QDragEnterEvent):
        # print("CalcSubMnd:: ~onDrop")
        # print("text: %s" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print("...denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event: QDragEnterEvent):
        # print("CalcSubMnd:: ~onDrag")
        # print("text: %s" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.nodeGraphicsScene.views()[0].mapToScene(mouse_position)

            # print("calaulator_subWindow:: GOT DROP: [%d] '%s" % (op_code, text), " mouse: ", mouse_position, "scene: ", scene_position)

            try:
                # node = Node_Calculator(self.scene , op_code, text, input=[1, 1], output=[1])
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
            except Exception as e:
                dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print("... drop igonred, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()