from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QPlainTextEdit

from ui.settingDialog import SettingDialog

PLACE_HOLDER_TEXT = \
"""请将log等级的定义粘贴至此进行解析。定义的位置可能位于camxdefs.h

示例:

static const CamxLogGroup CamxLogGroupAFD           = (static_cast<UINT64>(1) << 0);    ///< AFD
static const CamxLogGroup CamxLogGroupSensor        = (static_cast<UINT64>(1) << 1);    ///< Sensor
static const CamxLogGroup CamxLogGroupTracker       = (static_cast<UINT64>(1) << 2);    ///< Tracker
static const CamxLogGroup CamxLogGroupISP           = (static_cast<UINT64>(1) << 3);    ///< ISP
static const CamxLogGroup CamxLogGroupPProc         = (static_cast<UINT64>(1) << 4);    ///< Post Processor

......
"""

class LogLevelParsePanel(SettingDialog):

    def __init__(self, parent, size, module):
        super().__init__(parent, size)
        self.__module = module

    def setupUi(self, Dialog):
        self.__plainTextEdit_parser = QPlainTextEdit(self)
        self.__plainTextEdit_parser.setObjectName(u"plainTextEdit_parser")

        self._verticalLayout_main.addWidget(self.__plainTextEdit_parser)

        super().setupUi(Dialog)

    def retranslateUi(self, Dialog):
        super().retranslateUi(Dialog)
        Dialog.setWindowTitle(QCoreApplication.translate("SetingDialog", u"log等级解析", None))
        self.__plainTextEdit_parser.setPlaceholderText(QCoreApplication.translate("SetingDialog", PLACE_HOLDER_TEXT, None))
        self._pushButton_apply.setText(QCoreApplication.translate("SetingDialog", u"解析", None))

    def _reset(self):
        self.__plainTextEdit_parser.clear()

    def _cancel(self):
        self._reset()
        self.close()
