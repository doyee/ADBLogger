import requests

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.noWindowHintDialog import NoWindowDialog

from utils.UIUtils import *
from utils.Utils import *

from module.sqlManager import SQLManager

TIMEOUT = 20 # sec
GIT_API_URL = "https://api.github.com/repos/%s/%s/releases/latest" % (GIT_ACCOUNT, GIT_REPO)


class DownloadThread(QThread):
    downloadStart = pyqtSignal()
    downloadDone = pyqtSignal(bool)

    def __init__(self, path, url, size, parent=None):
        super().__init__(parent)
        self.__path = path
        self.__url = url
        self.__size = size

    def run(self) -> None:
        try:
            resp = requests.get(self.__url, stream=True, timeout=TIMEOUT)
            total = int(resp.headers.get("content-length", 0))
            if not self.__size == total:
                IF_Print("network error: size not match [total:%d - content:%d]" % (self.__size, total))
                self.downloadDone.emit(False)
                return
            IF_Print("\nStart Download at %s" % self.__url)

            with open(self.__path, "wb") as fp:
                self.downloadStart.emit()

                for data in resp.iter_content(chunk_size=1024):
                    try:
                        fp.write(data)
                    except Exception as e:
                        IF_Print("\nwriting failed: %s %s" % (self.__path, e))
                        self.downloadDone.emit(False)

                fp.close()
                self.downloadDone.emit(True)


        except:
            IF_Print("\nnetwork error: cannot GET from %s Timeout: %d sec" % (self.__url, TIMEOUT))
            self.downloadDone.emit(False)

class AutoUpdate(QObject):


    def __init__(self, listener):
        self.__db = SQLManager.get_instance()
        self.__latestReleaseInfo = {}
        size = GetWindowSize()
        self.__checkUpdateDialog = UpdateDialog((size[0] / 4, size[1] / 6), self)

    def CheckUpdate(self, isForce=False):

        self.__latestReleaseInfo = requests.get(url=GIT_API_URL).json()
        latestVersion = self.__latestReleaseInfo["tag_name"]
        isUpdate, latestVersion = self.__checkVersion(latestVersion)
        return isUpdate, latestVersion

    def Download(self):
        name, url, size = self.__parseAssets(self.__latestReleaseInfo["assets"])
        path = JoinPath(JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR), name)
        return path, url, size

    def Install(self):
        IF_Print("Start to Install")
        pass

    def __checkVersion(self, version):
        v = re.findall("\d+.\d+.\d+.\d+", version)[0]
        latestVersion = v.rsplit('.')
        curVersion = VERSION.rsplit(".")
        if (latestVersion[0] > curVersion[0]) \
                or (latestVersion[0] == curVersion[0] and latestVersion[1] > curVersion[1]) \
                or (latestVersion[0] == curVersion[0] and latestVersion[1] == curVersion[1] and latestVersion[2] >
                    curVersion[2]) \
                or (latestVersion[0] == curVersion[0] and latestVersion[1] == curVersion[1] and latestVersion[2] ==
                    curVersion[2] and latestVersion[3] > curVersion[3]):
            return True, v
        return False, v

    def __parseAssets(self, assetInfo):
        runnableSuffix = GetRunnableSuffix()
        for asset in assetInfo:
            if len(re.findall(".*%s" % runnableSuffix, asset["name"])) > 0:
                return asset["name"], asset["browser_download_url"], int(asset["size"])


class UpdateDialog(NoWindowDialog):

    def __init__(self, displaySize, module, parent=None):
        super(UpdateDialog, self).__init__(parent)
        self.__downloadDialog = DownloadDialog((displaySize[0] / 4, displaySize[1] / 8))
        self.__size = (displaySize[0] / 4, displaySize[1] / 6)
        self.__module = module
        self.__isForce = False
        self.setupUi(self)

    def show(self, latestVersion) -> None:
        self.__latestVersion = latestVersion
        self.label_latestVersion.setText(QCoreApplication.translate("Dialog",
                                                                    u"\u6700\u65b0\u53ef\u66f4\u65b0\u7248\u672c\uff1a%s" % self.__latestVersion,
                                                                    None))
        self.checkBox_ignoreVersion.setHidden(self.__isForce)
        super().show()


    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(self.__size[0], self.__size[1])
        Dialog.setMaximumSize(self.__size[0], self.__size[1])
        Dialog.setMinimumSize(self.__size[0], self.__size[1])
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
        self.checkBox_ignoreVersion.clicked.connect(self.__checkIgnore)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"在线更新", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"\u53d1\u73b0\u65b0\u7248\u672c\uff01", None))
        self.label_curVersion.setText(
            QCoreApplication.translate("Dialog", u"\u5f53\u524d\u7248\u672c\uff1a%s" % VERSION, None))
        self.checkBox_ignoreVersion.setText(
            QCoreApplication.translate("Dialog", u"\u5ffd\u7565\u8be5\u7248\u672c\u66f4\u65b0\u63d0\u9192", None))
        self.pushButton_ignore.setText(QCoreApplication.translate("Dialog", u"\u6682\u4e0d\u66f4\u65b0", None))
        self.pushButton_update.setText(QCoreApplication.translate("Dialog", u"\u7acb\u5373\u66f4\u65b0", None))

    # retranslateUi

    def SetIsForce(self, isForce):
        self.__isForce = isForce

    def __ignore(self):
        self.close()

    def __update(self):
        path, url, size = self.__module.Download()
        download = DownloadThread(path, url, size)
        download.downloadStart.connect(self.__onDownloadStart)
        download.downloadDone.connect(self.__onDownloadDone)
        download.start()
        self.close()
        self.__downloadDialog.show(path, size)

    def __checkIgnore(self, checked):
        self.pushButton_update.setEnabled(not checked)


    def __onDownloadStart(self):
        self.__downloadDialog.Start()

    def __onDownloadDone(self, isSuccess):
        self.__downloadDialog.Stop(isSuccess)
        if isSuccess:
            ShowMessageDialog(MESSAGE_TYPE_INFO, MESSAGE_STR_DOWNLOAD_DONE_AND_INSTALL)
            self.__module.Install()
            self.__downloadDialog.close()
        else:
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_NETWORK_ERROR)
            self.__downloadDialog.close()
            self.show(self.__latestVersion)

DOWNLOAD_TIMER_STEP = 1000  # ms


class DownloadDialog(NoWindowDialog):
    def __init__(self, size, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self.__size = size
        self.__timer = None
        self.__path = ""
        self.__startTime = 0
        self.__fileSize = 0
        self.__shouldUpdateProgress = False
        self.setupUi(self)
        self.__updateFlagMutex = QMutex()

    def show(self, path, fileSize) -> None:
        super().show()
        self.__path = path
        self.__fileSize = fileSize
        self.__timer = QBasicTimer()
        self.__timer.start(DOWNLOAD_TIMER_STEP, self)
        self.__time = time.time()

    def close(self) -> bool:
        self.__reset()
        return super(DownloadDialog, self).close()

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(self.__size[0], self.__size[1])
        Dialog.setMaximumSize(self.__size[0], self.__size[1])
        Dialog.setMinimumSize(self.__size[0], self.__size[1])
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, self.__size[0], self.__size[1]))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 0, 10)
        self.labeltitle = QLabel(self.verticalLayoutWidget)
        self.labeltitle.setObjectName(u"labeltitle")

        self.verticalLayout.addWidget(self.labeltitle)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

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

        self.label_time_left = QLabel(self.verticalLayoutWidget)
        self.label_time_left.setObjectName(u"label_time_left")
        sizePolicy.setHeightForWidth(self.label_time_left.sizePolicy().hasHeightForWidth())
        self.label_time_left.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_time_left)

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
        self.label_time_left.setText(
            QCoreApplication.translate("Dialog", u"\u9884\u8ba1\u5269\u4f59\u65f6\u95f4:", None))
        # retranslateUi

    def Start(self):
        self.__updateFlagMutex.lock()
        self.__shouldUpdateProgress = True
        self.__startTime = time.time_ns()
        self.__updateFlagMutex.unlock()
        IF_Print("start downloading dialog: %f" % self.__startTime)

    def Stop(self, isDone):
        self.__updateFlagMutex.lock()
        self.__shouldUpdateProgress = False
        self.__updateFlagMutex.unlock()
        IF_Print("\nstop downloading.")
        self.__resetLabels()
        if isDone:
            self.progressBar.setValue(100)
        self.__timer.stop()

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.__updateProgress()

    def __updateProgress(self):
        print("\rcheck flag %d time = %d sec" % (self.__shouldUpdateProgress, (time.time() - self.__time)), end="")
        if not self.__shouldUpdateProgress:
            return
        curTime = time.time_ns()
        curSize = float(os.path.getsize(self.__path))
        percentage = curSize / float(self.__fileSize) * 100
        self.progressBar.setValue(int(percentage))

        speed = curSize / ((curTime - self.__startTime) / 1000 / 1000 / 1000)

        if not speed == 0:
            remain = self.__fileSize - curSize
            remainTime = remain / speed  # in seconds

            speedLabel = "%.2f byte/s" % speed
            if speed > 1024:
                speed = (speed / 1024)
                speedLabel = "%.2f KB/s" % speed
                if speed > 1024:
                    speed = speed / 1024
                    speedLabel = "%.2f MB/s" % speed
                    if speed > 1024:
                        speed = speed / 1024
                        speedLabel = "%.2f GB/s" % speed

            h = int(remainTime / 3600)
            min = int((remainTime - h * 3600 ) / 60)
            sec = int(remainTime - (h * 3600 + 60 * min))
            remainTimeLabel = "%02d:%02d:%02d" % (h, min, sec)
        else:
            speedLabel = "0 bytes/s"
            remainTimeLabel = "??:??:??"
        self.__updateLabels(speedLabel, remainTimeLabel)

    def __updateLabels(self, speedLabelText, restTimeLabelText):
        self.label_download_speed.setText(
            QCoreApplication.translate("Dialog", u"\u5f53\u524d\u4e0b\u8f7d\u901f\u5ea6: %s" % speedLabelText, None))
        self.label_time_left.setText(
            QCoreApplication.translate("Dialog", u"\u9884\u8ba1\u5269\u4f59\u65f6\u95f4: %s" % restTimeLabelText, None))

    def __resetLabels(self):
        self.label_download_speed.setText(
            QCoreApplication.translate("Dialog", u"\u5f53\u524d\u4e0b\u8f7d\u901f\u5ea6:", None))
        self.label_time_left.setText(
            QCoreApplication.translate("Dialog", u"\u9884\u8ba1\u5269\u4f59\u65f6\u95f4:", None))

    def __reset(self):
        self.__startTime = 0
        self.__fileSize = 0
        self.__shouldUpdateProgress = False
        self.progressBar.setValue(0)
        self.__resetLabels()
