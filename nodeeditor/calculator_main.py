import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory

from CalculatorWindow.calculator_window import CalculatorMainWindow
from memory_profiler import profile

@profile
def main():
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    # app.setStyle('Fusion')    修改不同樣式

    window = CalculatorMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
