from utils.Utils import *

from PyQt5.QtCore import Qt, QBasicTimer, QCoreApplication, QTimerEvent, QMutex
from PyQt5.QtWidgets import QDialog
from ui.DownloadDialog import Ui_DownloadDialog as UiDownload


DOWNLOAD_TIMER_STEP = 1000  # ms


# noinspection PyMethodOverriding
class DownloadDialog(QDialog, UiDownload):
    def __init__(self, parent=None):
        super(DownloadDialog, self).__init__(parent)
        super().setupUi(self)
        self.__startTime = None
        self.__shouldUpdateProgress = False
        self.__updateFlagMutex = QMutex()
        self.__time = None
        self.__timer = None
        self.__fileSize = None
        self.__path = None
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.Dialog)

    def show(self, filePath, fileSize):
        super().show()
        self.__path = filePath
        self.__fileSize = fileSize
        self.__timer = QBasicTimer()
        self.__timer.start(DOWNLOAD_TIMER_STEP, self)
        self.__time = time.time()

    def close(self) -> bool:
        self.__reset()
        return super(DownloadDialog, self).close()

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

    def timerEvent(self, a0: 'QTimerEvent'):
        self.__updateProgress()

    def __updateProgress(self):
        # loggingInfo = "check shouldUpdateProgress:%d " % self.__shouldUpdateProgress
        # loggingInfo += loggingInfo + "time: %d seconds" % (time.time() - self.__time)
        # IF_Print(loggingInfo)
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
            minutes = int((remainTime - h * 3600) / 60)
            sec = int(remainTime - (h * 3600 + 60 * minutes))
            remainTimeLabel = "%02d:%02d:%02d" % (h, minutes, sec)
        else:
            speedLabel = "0 bytes/s"
            remainTimeLabel = "??:??:??"
        self.__updateLabels(speedLabel, remainTimeLabel)

    def __updateLabels(self, speedLabelText, restTimeLabelText):
        text = self.label_download_speed.accessibleName()
        self.label_download_speed.setText(
            QCoreApplication.translate("DownloadDialog", text + speedLabelText, None))
        text = self.label_time_left.accessibleName()
        self.label_time_left.setText(
            QCoreApplication.translate("DownloadDialog", text + restTimeLabelText, None))

    def __resetLabels(self):
        text = self.label_download_speed.accessibleName()
        self.label_download_speed.setText(
            QCoreApplication.translate("DownloadDialog", text, None))

        text = self.label_time_left.accessibleName()
        self.label_time_left.setText(
            QCoreApplication.translate("DownloadDialog", text, None))

    def __reset(self):
        self.__startTime = 0
        self.__fileSize = 0
        self.__shouldUpdateProgress = False
        self.progressBar.setValue(0)
        self.__resetLabels()
