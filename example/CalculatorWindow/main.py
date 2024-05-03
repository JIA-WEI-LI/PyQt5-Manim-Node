import sys
from PyQt5.QtWidgets import QApplication

from calculator_wondow import CalaulatorMainWindow
from memory_profiler import profile

@profile
def main():
    app = QApplication(sys.argv)
    window = CalaulatorMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
