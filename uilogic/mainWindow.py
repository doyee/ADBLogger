import threading
from ctypes import wintypes
from time import sleep

import win32con
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from module.adbManager import ADBManager
from module.autoUpdate import AutoUpdate
from module.generalSetings import GeneralSettings
from module.levelModule import LevelModule
from module.logLevelParser import LogLevelParser
from module.pullModule import PullModule
from ui.UIMainWindow import Ui_MainWindow as UIM
from uilogic.logLevelParserPanel import LogLevelParserPanel
from uilogic.logLevelTabFrame import LogLevelTabFrame
from uilogic.logPullTabFrame import LogPullTabFrame
from uilogic.aboutDialog import AboutDialog
from uilogic.upgradeDialog import UpgradeDialog
from utils.UIUtils import *
from utils.Utils import *

TITLE_PREFIX = "AndroidLogs"


class AutoUpdateThread(QThread):
    versionChecked = pyqtSignal(bool, str)

    def __init__(self, autoUpdate, parent=None):
        super().__init__(parent)
        self.__update = autoUpdate
        self.__isForce = False

    def SetIsForce(self, isForce):
        self.__isForce = isForce

    def GetAutoUpdateInstance(self):
        return self.__update

    def run(self) -> None:
        hasNewVersion, latestVersion = self.__update.CheckUpdate(self.__isForce)
        self.versionChecked.emit(hasNewVersion, latestVersion)


class MainWindow(QMainWindow, UIM):
    class DeviceThread(threading.Thread):
        def __init__(self, adbManager, comboBox, callback, delay):
            threading.Thread.__init__(self)
            self.__adbManager = adbManager
            self.__comboBox = comboBox
            self.__callback = callback
            self.__delay = delay

        def run(self):
            sleep(self.__delay)

            deviceInfo = self.__adbManager.GetDeviceInfo(True)
            self.__comboBox.clear()
            if not deviceInfo == None:
                infos = []
                for info in deviceInfo:
                    infoStr = " %s: %s \t [Status:%s]" % (
                        info[DEVICE_INFO_NAME], info[DEVICE_INFO_ID], info[DEVICE_INFO_STATUS])
                    infos.append(infoStr)
                self.__comboBox.addItems(infos)
            self.__callback()

    device_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        UIM.__init__(self)
        self.__isChecking = False
        self.__adbManager = ADBManager.get_instance()
        self.__deviceInfo = []
        self.__displaySize = GetWindowSize()
        self.__autoUpdate = AutoUpdate()
        self.__updateThread = AutoUpdateThread(self.__autoUpdate)
        self.__autoUpgradeDialog = UpgradeDialog(self.__autoUpdate)
        self.__setupUi()
        self.__connectUi()

    def __buildTabs(self):
        settingModule = GeneralSettings()
        self.tab_log_pull.setObjectName(u"tab_log_pull")
        self.log_pull_frame = LogPullTabFrame(PullModule(settingModule), self.tab_log_pull)
        self.tabWidget_main.setCurrentWidget(self.tab_log_pull)
        self.log_pull_frame.buildUp()
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.log_pull_frame)
        self.tab_log_pull.setLayout(gridlayout)

        self.tab_log_level.setObjectName(u"tab_log_level")
        self.level_tab_frame = LogLevelTabFrame(LevelModule(), self.tab_log_level)
        self.level_tab_frame.buildUp()
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.level_tab_frame)
        self.tab_log_level.setLayout(gridlayout)

    def __buildParser(self):
        self.__parserDialog = LogLevelParserPanel(LogLevelParser(self.level_tab_frame))
        self.__parserDialog.buildUp()

    def __buildStatusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.addWidget(QLabel(GetVersionStr()), 1)
        self.__latestVersion = QLabel("")
        self.__latestVersion.setObjectName(u"LatestLabel")
        self.statusbar.addWidget(self.__latestVersion, 1)
        self.setStatusBar(self.statusbar)

    def __buildAbout(self):
        self.__aboutDialog = AboutDialog()
        self.__aboutDialog.buildUp()

    def __setupUi(self):
        self.setupUi(self)
        self.__updateDevice()
        self.__buildTabs()
        self.__buildParser()
        self.__buildStatusbar()
        self.__buildAbout()

    def show(self, isFirstTime):
        super().show()
        if isFirstTime:
            self.__parserDialog.show()
        self.__updateThread.start()

    def __connectUi(self):
        # menu
        self.action_log_level_settings.triggered.connect(self.__onMenu)
        self.action_check_upgrade.triggered.connect(self.__onMenu)
        self.action_refresh_device_list.triggered.connect(self.__onMenu)
        self.action_about.triggered.connect(self.__onMenu)

        self.__updateThread.versionChecked.connect(self.__onCheckUpdate)
        self.device_changed.connect(self.__onUSBStateChanged)
        self.pushButton_root.clicked.connect(self.__onRemount)
        self.pushButton_kill_cam.clicked.connect(self.__onKillCameraServer)

    def __onMenu(self):
        if self.sender() == self.action_log_level_settings:
            self.__parserDialog.show()
        elif (self.sender() == self.action_check_upgrade) and (not self.__isChecking):
            self.__isChecking = True
            self.__updateThread.SetIsForce(True)
            self.__updateThread.start()
        elif self.sender() == self.action_refresh_device_list:
            self.__updateDevice()
        elif self.sender() == self.action_about:
            self.__aboutDialog.show()

    def __updateDevice(self, delay=0):
        sleep(delay)

        self.__deviceInfo = self.__adbManager.GetDeviceInfo(True)
        self.comboBox_device_list.clear()
        if not self.__deviceInfo == None:
            infos = []
            for info in self.__deviceInfo:
                infoStr = " %s: %s \t [Status:%s]" % (
                info[DEVICE_INFO_NAME], info[DEVICE_INFO_ID], info[DEVICE_INFO_STATUS])
                infos.append(infoStr)
            self.comboBox_device_list.addItems(infos)
        self.__onDeviceChanged()

    def __onRemount(self):
        res = self.__adbManager.Remount()
        t, m = ErrorCodeToMessage(res)
        ShowMessageDialog(t, m)

    def __onKillCameraServer(self):
        res = self.__adbManager.KillCameraServer()
        t, m = ErrorCodeToMessage(res)
        ShowMessageDialog(t, m)

    def __onDeviceChanged(self):
        currentSelected = self.comboBox_device_list.currentIndex()
        if currentSelected == -1:
            title = TITLE_PREFIX
        else:
            title = "%s - %s (%s)" % (TITLE_PREFIX, self.__deviceInfo[currentSelected][DEVICE_INFO_ID],
                                      self.__deviceInfo[currentSelected][DEVICE_INFO_STATUS])
        self.setWindowTitle(QCoreApplication.translate("MainWindow", title, None))
        self.__adbManager.SetSelectedDevice(currentSelected)

    def __onUSBStateChanged(self):
        self.__updateDevice(delay=0.5)

    def nativeEvent(self, eventType, message):
        retval, result = super().nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_DEVICECHANGE:
                self.device_changed.emit()

        return retval, result

    def __onCheckUpdate(self, hasNewVersion, latestVersion):
        if hasNewVersion:
            self.__autoUpgradeDialog.show(latestVersion)

        self.__isChecking = False
        self.__latestVersion.setText("最新版本:%s" % latestVersion)
