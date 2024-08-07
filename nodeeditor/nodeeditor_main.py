import os
import sys
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from NodeEditorWindow.NodeEditor.nodeEditor_Window import NodeEditorMainWindow
from memory_profiler import profile

@profile
def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window = NodeEditorMainWindow()
    window.nodeEditor.addNodes()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()