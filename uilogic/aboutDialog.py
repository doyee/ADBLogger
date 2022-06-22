from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from ui.About import Ui_aboutWiget as About
from utils.defines import VERSION


class AboutDialog(QWidget, About):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.Dialog)

    def __setUpUI(self):
        self.setupUi(self)
        name_version = self.lable_name.accessibleName() + "  v" + VERSION
        self.lable_name.setText(name_version)

    def buildUp(self):
        self.__setUpUI()
