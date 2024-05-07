import os
import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from CalculatorWindow.calculator_window import CalculatorMainWindow
from memory_profiler import profile

@profile
def main():
    # HACK:  + ['-platform', 'windows:darkmode=1'] 可使用 window 內建的暗黑模式
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])

    # print(QStyleFactory.keys())
    # app.setStyle('Fusion')    修改不同樣式

    window = CalculatorMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
