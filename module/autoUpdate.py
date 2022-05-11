import time

import requests
import os, re
from utils.defines import *
from utils.UIUtils import *
from utils.Utils import *

from module.sqlManager import SQLManager
GIT_API_URL = "https://api.github.com/repos/%s/%s/releases/latest" % (GIT_ACCOUNT, GIT_REPO)

class AutoUpdate(object):
    def __init__(self):
        self.__db = SQLManager.get_instance()
        self.__latestReleaseInfo = {}
        size = GetWindowSize()
        self.__checkUpdateDialog = UpdateDialog((size[0] / 4, size[1] / 6), self)
        self.__downloadDialog = DownloadDialog((size[0]/ 4, size[1]/ 8))

    def CheckUpdate(self, isForce=False):
        self.__latestReleaseInfo = requests.get(url=GIT_API_URL).json()
        latestVersion = self.__latestReleaseInfo["tag_name"]
        isUpdate, latestVersion = self.__checkVersion(latestVersion)
        if (isUpdate):
            self.__checkUpdateDialog.show(latestVersion)

    def Download(self):
        path = JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR)
        print(path)
        self.__downloadDialog.show()

    def __checkVersion(self, version):
        v = re.findall("\d+.\d+.\d+.\d+", version)[0]
        latestVersion = v.rsplit('.')
        curVersion = VERSION.rsplit(".")
        print(latestVersion, curVersion)
        if (latestVersion[0] > curVersion[0]) \
                or (latestVersion[0] == curVersion[0] and latestVersion[1] > curVersion[1])\
                or (latestVersion[0] == curVersion[0] and latestVersion[1] == curVersion[1] and latestVersion[2] > curVersion[2]) \
                or (latestVersion[0] == curVersion[0] and latestVersion[1] == curVersion[1] and latestVersion[2] == curVersion[2] and latestVersion[3] > curVersion[3]):
            return True, v
        return False, v


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.noWindowHintDialog import NoWindowDialog

class UpdateDialog(NoWindowDialog):

    def __init__(self, size, module, parent=None):
        super(UpdateDialog, self).__init__(parent)
        self.__size = size
        self.__module = module

    def show(self, latestVersion) -> None:
        self.__latestVersion = latestVersion
        self.setupUi(self)
        super().show()

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(self.__size[0], self.__size[1])
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, self.__size[0], self.__size[1]))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.label_title = QLabel(self.verticalLayoutWidget)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(15)
        self.label_title.setFont(font)
        self.label_title.setCursor(QCursor(Qt.UpArrowCursor))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_title)

        self.label_latestVersion = QLabel(self.verticalLayoutWidget)
        self.label_latestVersion.setObjectName(u"label_latestVersion")

        self.verticalLayout.addWidget(self.label_latestVersion)

        self.label_curVersion = QLabel(self.verticalLayoutWidget)
        self.label_curVersion.setObjectName(u"label_curVersion")

        self.verticalLayout.addWidget(self.label_curVersion)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_ignoreVersion = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_ignoreVersion.setObjectName(u"checkBox_ignoreVersion")

        self.horizontalLayout.addWidget(self.checkBox_ignoreVersion)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ignore = QPushButton(self.verticalLayoutWidget)
        self.pushButton_ignore.setObjectName(u"pushButton_ignore")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ignore.sizePolicy().hasHeightForWidth())
        self.pushButton_ignore.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_ignore)

        self.pushButton_update = QPushButton(self.verticalLayoutWidget)
        self.pushButton_update.setObjectName(u"pushButton_update")
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_update)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.__connectUI()
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def __connectUI(self):
        self.pushButton_ignore.clicked.connect(self.__ignore)
        self.pushButton_update.clicked.connect(self.__update)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"在线更新", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"\u53d1\u73b0\u65b0\u7248\u672c\uff01", None))
        self.label_latestVersion.setText(QCoreApplication.translate("Dialog", u"\u6700\u65b0\u53ef\u66f4\u65b0\u7248\u672c\uff1a%s" % self.__latestVersion, None))
        self.label_curVersion.setText(QCoreApplication.translate("Dialog", u"\u5f53\u524d\u7248\u672c\uff1a%s" % VERSION, None))
        self.checkBox_ignoreVersion.setText(QCoreApplication.translate("Dialog", u"\u5ffd\u7565\u8be5\u7248\u672c\u66f4\u65b0\u63d0\u9192", None))
        self.pushButton_ignore.setText(QCoreApplication.translate("Dialog", u"\u6682\u4e0d\u66f4\u65b0", None))
        self.pushButton_update.setText(QCoreApplication.translate("Dialog", u"\u7acb\u5373\u66f4\u65b0", None))
    # retranslateUi

    def __ignore(self):
        self.close()

    def __update(self):
        self.__module.Download()
        self.close()

DOWNLOAD_TIMER_STEP = 100  # ms

class DownloadDialog(NoWindowDialog):
    def __init__(self, size, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self.__size = size
        self.__timer = None
        self.setupUi(self)

    def show(self) -> None:
        super().show()
        self.__timer = QBasicTimer()
        self.__timer.start(DOWNLOAD_TIMER_STEP, self)


    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(self.__size[0], self.__size[1])
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, self.__size[0], self.__size[1]))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.labeltitle = QLabel(self.verticalLayoutWidget)
        self.labeltitle.setObjectName(u"labeltitle")

        self.verticalLayout.addWidget(self.labeltitle)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_download_speed = QLabel(self.verticalLayoutWidget)
        self.label_download_speed.setObjectName(u"label_download_speed")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_download_speed.sizePolicy().hasHeightForWidth())
        self.label_download_speed.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_download_speed)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_4)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

        # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"在线更新", None))
        self.labeltitle.setText(
            QCoreApplication.translate("Dialog", u"\u6b63\u5728\u4e0b\u8f7d\uff0c\u8bf7\u7a0d\u540e...", None))
        self.label_download_speed.setText(
            QCoreApplication.translate("Dialog", u"\u5f53\u524d\u4e0b\u8f7d\u901f\u5ea6:", None))
        self.label_4.setText(
            QCoreApplication.translate("Dialog", u"\u9884\u8ba1\u5269\u4f59\u65f6\u95f4\uff1a", None))
        # retranslateUi



    def timerEvent(self, a0: 'QTimerEvent') -> None:
        print(time.time(), "helloworld" )
        self.__updateProgress()

    def __updateProgress(self):
        pass


