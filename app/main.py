import sys
from PyQt5.QtWidgets import QApplication

from NodeEditor.nodeEditor_Widget import NodeEditorWidget

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = NodeEditorWidget()

    sys.exit(app.exec_())