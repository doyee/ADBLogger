from PyQt5.QtWidgets import QLineEdit


class DropLineEditor(QLineEdit):
    def __init__(self, parent=None):
        super(DropLineEditor, self).__init__(parent)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().urls()[0].path()[1:])