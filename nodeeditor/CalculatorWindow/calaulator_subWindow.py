from PyQt5.QtCore import Qt
from NodeEditorWindow.nodeEditor_Widget import NodeEditorWidget

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

    def onDragEnter(self, event):
        print("CalcSubMnd:: ~onDrop")
        print("text: %s" % event.mimeData().text())

    def onDrop(self, event):
        print("CalcSubMnd:: ~onDrag")
        print("text: %s" % event.mimeData().text())