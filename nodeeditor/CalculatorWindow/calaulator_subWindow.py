from PyQt5.QtCore import Qt
from NodeEditorWindow.nodeEditor_Widget import NodeEditorWidget

class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())