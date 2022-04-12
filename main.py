import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui.mainWindow import MainWindow
if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())