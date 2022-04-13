from abc import abstractmethod

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SettingDialog(QDialog):

    def __init__(self, parent, size):
        super(SettingDialog, self).__init__(parent)
        self.__size = size

        self._verticalLayout_main = QVBoxLayout(self)
        self._verticalLayout_main.setObjectName(u"_verticalLayout_main")
        self._verticalLayout_main.setContentsMargins(10, 10, 10, 10)

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(self.__size[0], self.__size[1])
        # self.verticalLayoutWidget = QWidget(Dialog)
        # self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        # self.verticalLayoutWidget.setGeometry(QRect(0, 0, self.__size[0], self.__size[1]))

        self.__horizontalLayout_buttons = QHBoxLayout()
        self.__horizontalLayout_buttons.setObjectName(u"__horizontalLayout_buttons")
        self._pushButton_reset = QPushButton(self)
        self._pushButton_reset.setObjectName(u"__pushButton_reset")

        self.__horizontalLayout_buttons.addWidget(self._pushButton_reset)

        self.__horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.__horizontalLayout_buttons.addItem(self.__horizontalSpacer)

        self._pushButton_cancel = QPushButton(self)
        self._pushButton_cancel.setObjectName(u"__pushButton_cancel")

        self.__horizontalLayout_buttons.addWidget(self._pushButton_cancel)

        self._pushButton_apply = QPushButton(self)
        self._pushButton_apply.setObjectName(u"__pushButton_apply")

        self.__horizontalLayout_buttons.addWidget(self._pushButton_apply)


        self._verticalLayout_main.addLayout(self.__horizontalLayout_buttons)


        self.retranslateUi(Dialog)
        self._connectUi()

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        self._pushButton_reset.setText(QCoreApplication.translate("SetingDialog", u"重置", None))
        self._pushButton_cancel.setText(QCoreApplication.translate("SetingDialog", u"取消", None))

    # retranslateUi

    def _connectUi(self):
        self._pushButton_reset.clicked.connect(self._onButtonClicked)
        self._pushButton_cancel.clicked.connect(self._onButtonClicked)
        self._pushButton_apply.clicked.connect(self._onButtonClicked)

    def _onButtonClicked(self):
        if self.sender() == self._pushButton_cancel:
            self._cancel()
        elif self.sender() == self._pushButton_apply:
            self._apply()
        elif self.sender() == self._pushButton_reset:
            self._reset()

    @abstractmethod
    def _reset(self):
        pass

    @abstractmethod
    def _apply(self):
        pass

    @abstractmethod
    def _cancel(self):
        pass


    def closeEvent(self, a0):
        self._reset()
        super(SettingDialog, self).closeEvent(a0)