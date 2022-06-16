from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class NoWindowDialog(QDialog):
    def __init__(self, parent=None):
        super(NoWindowDialog, self).__init__(parent)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.Dialog)
