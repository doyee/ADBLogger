from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QPlainTextEdit, QDialog

from ui.LogLevelParserPanel import Ui_LogLevelParserPanel as UILLPP
from uilogic.noWindowHintDialog import NoWindowDialog
from utils.UIUtils import *

PLACE_HOLDER_TEXT = \
"""请将log等级的定义粘贴至此进行解析。定义的位置可能位于camxdefs.h

示例:

static const CamxLogGroup CamxLogGroupAFD           = (static_cast<UINT64>(1) << 0);    ///< AFD
static const CamxLogGroup CamxLogGroupSensor        = (static_cast<UINT64>(1) << 1);    ///< Sensor
static const CamxLogGroup CamxLogGroupTracker       = (static_cast<UINT64>(1) << 2);    ///< Tracker
static const CamxLogGroup CamxLogGroupISP           = (static_cast<UINT64>(1) << 3);    ///< ISP
static const CamxLogGroup CamxLogGroupPProc         = (static_cast<UINT64>(1) << 4);    ///< Post Processor
static const CamxLogGroup CamxLogGroupPProc2        = CamxLogGroupPProc            ;    ///< Post Processor
......
"""


class LogLevelParserPanel(NoWindowDialog, UILLPP):

    def __init__(self, module):
        super().__init__()
        self.__module = module

    def buildUp(self):
        self.__setupUi()
        self.__connectUi()

    def __setupUi(self):
        self.setupUi(self)
        self.plainTextEdit.setPlaceholderText(
            QCoreApplication.translate("LogLevelParserPanel", PLACE_HOLDER_TEXT, None))

    def __connectUi(self):
        self.pushButton_reset.clicked.connect(self.__OnReset)
        self.pushButton_cancel.clicked.connect(self.__OnCancel)
        self.pushButton_apply.clicked.connect(self.__OnApply)

    def __OnReset(self):
        self.plainTextEdit.clear()

    def __OnCancel(self):
        self.__OnReset()
        self.close()

    def __OnApply(self):
        text = self.plainTextEdit.toPlainText()
        if text == "":
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_PARSER_EMPTY_INPUT)
            return

        res = self.__module.Parse(text)
        self.__ShowMessage(res)

    def __ShowMessage(self, errorCode):
        if errorCode == ERROR_CODE_SUCCESS:
            ShowMessageDialog(MESSAGE_TYPE_INFO, MESSAGE_STR_SUCCESS)
        elif errorCode == ERROR_CODE_INVALID_PARAM:
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_INVALID_PARAM)
        elif errorCode == ERROR_CODE_DB_INSERT_FAILED:
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_DB_INSERT_FAILED)
