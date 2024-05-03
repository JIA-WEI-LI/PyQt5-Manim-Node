import sys
from PyQt5.QtWidgets import QApplication

from NodeEditorWindow.nodeEditor_Window import NodeEditorMainWindow
from memory_profiler import profile

@profile
def main():
    app = QApplication(sys.argv)
    window = NodeEditorMainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
