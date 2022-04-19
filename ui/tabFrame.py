from abc import abstractmethod

from PyQt5.QtWidgets import QFrame
from module.toolModule import ToolModule

class TabFrame(QFrame):

    def __init__(self, module, parent=None):
        super(TabFrame, self).__init__(parent)
        self._module = module

    @abstractmethod
    def layoutFrame(self):
        self._connectUi()
        self._retranslateUi()

    @abstractmethod
    def _connectUi(self):
        pass

    @abstractmethod
    def _retranslateUi(self):
        pass