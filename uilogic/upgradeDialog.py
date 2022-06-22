from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from module.autoUpdate import AutoUpdate, DownloadThread
from ui.UpgradeDialog import Ui_UpgradeDialog as UD
from uilogic.downloadDialog import DownloadDialog
from utils.defines import *
from utils.UIUtils import *


class UpgradeDialog(QDialog, UD):
    def __init__(self, autoUpdate, parent=None):
        super(UpgradeDialog, self).__init__(parent)
        super().setupUi(self)
        self.__autoUpdate = autoUpdate
        self.__downloadDialog = DownloadDialog()
        self.__latestVersion  = VERSION
        self.__downloading = False
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.Dialog)

    def show(self, latestVersion):
        name_version = self.lable_curr_version.accessibleName() + " v" + VERSION
        self.lable_curr_version.setText(name_version)
        name_version = self.label_latest_version.accessibleName() + " v" + latestVersion
        self.label_latest_version.setText(name_version)
        self.__latestVersion = latestVersion

        if self.__downloading:
            self.__downloadDialog.activateWindow()
        else:
            super().show()

    def showDownload(self):
        path, url, size = self.__autoUpdate.Download()
        download = DownloadThread(path, url, size)
        download.downloadStart.connect(self.__onDownloadStart)
        download.downloadDone.connect(self.__onDownloadDone)
        download.start()
        self.close()
        self.__downloading = True
        self.__downloadDialog.show(path, size)

    def ignoreThisVersion(self):
        self.__autoUpdate.IgnoreVersion(self.__latestVersion)
        self.close()

    def __onDownloadStart(self):
        self.__downloadDialog.Start()

    def __onDownloadDone(self, success, path):
        self.__downloading = False
        self.__downloadDialog.Stop(success)
        if success:
            ShowMessageDialog(MESSAGE_TYPE_INFO, MESSAGE_STR_DOWNLOAD_DONE_AND_INSTALL)
            self.__downloadDialog.close()
            self.__autoUpdate.Install(path)
        else:
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_NETWORK_ERROR)
            self.__downloadDialog.close()
            self.show(self.__latestVersion)
