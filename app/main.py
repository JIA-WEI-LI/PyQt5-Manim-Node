import sys
from PyQt5.QtWidgets import QApplication

from Node.nodeEditor_Window import NodeEditorWindow

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = NodeEditorWindow()

    sys.exit(app.exec_())