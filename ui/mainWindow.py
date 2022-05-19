import threading
from ctypes import wintypes
from time import sleep

import win32con
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from module.adbManager import ADBManager
from utils.UIUtils import *
from ui.logLevelTabFrame import LogLevelTabFrame
from ui.logPullTabFrame import LogPullTabFrame
from ui.logLevelParsePanel import LogLevelParsePanel
from ui.generalSettingPanel import GeneralSettingPanel
from module.levelModule import LevelModule
from module.pullModule import PullModule
from module.logLevelParser import LogLevelParser
from module.generalSetings import GeneralSettings
from module.autoUpdate import AutoUpdate, UpdateDialog
from utils.Utils import *

TITLE_PREFIX = "adb logcat tool"


class AutoUpdateThread(QThread):
    versionChecked = pyqtSignal(bool, str)

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.__module = module
        self.__isForce = False

    def SetIsForce(self, isForce):
        self.__isForce = isForce

    def run(self) -> None:
        hasNewVersion, latestVersion = self.__module.CheckUpdate(self.__isForce)
        self.versionChecked.emit(hasNewVersion, latestVersion)

class MainWindow(QMainWindow):

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
        self.__isChecking = False
        QWidget.__init__(self, parent)
        self.__adbManager = ADBManager.get_instance()
        self.__deviceInfo = []
        self.__displaySize = GetWindowSize()
        self.__autoUpdateModule = AutoUpdate(self)
        self.__updateThread = AutoUpdateThread(self.__autoUpdateModule)
        self.setupUi(self, (self.__displaySize[0] / 3, self.__displaySize[1] * 3 / 5))

    def setupUi(self, MainWindow, windowSize):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(windowSize[0], windowSize[1])
        MainWindow.setMaximumSize(windowSize[0], windowSize[1])
        MainWindow.setMinimumSize(windowSize[0], windowSize[1])
        MainWindow.setWindowIcon(QIcon('icon/icon.ico'))
        IF_Print("windowSize = %d,%d" % (windowSize[0], windowSize[1]))

        self.action_general_settings = QAction(MainWindow)
        self.action_general_settings.setObjectName(u"action_general_settings")
        self.action_log_level_settings = QAction(MainWindow)
        self.action_log_level_settings.setObjectName(u"action_log_level_settings")
        self.action_check_update = QAction(MainWindow)
        self.action_check_update.setObjectName(u"action_check_update")
        self.action_refresh_device_list = QAction(MainWindow)
        self.action_refresh_device_list.setObjectName(u"action_refresh_device_list")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, windowSize[0], windowSize[1]))
        self.verticalLayout_main = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(0, 10, 0, 10)
        self.horizontalLayout_device = QHBoxLayout()
        self.horizontalLayout_device.setObjectName(u"horizontalLayout_device")
        self.horizontalLayout_device.setContentsMargins(10, 0, 10, 0)
        self.label_device = QLabel(self.verticalLayoutWidget)
        self.label_device.setObjectName(u"label_device")

        self.horizontalLayout_device.addWidget(self.label_device)

        self.comboBox_device_list = QComboBox(self.verticalLayoutWidget)
        self.comboBox_device_list.setObjectName(u"comboBox_device_list")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_device_list.sizePolicy().hasHeightForWidth())
        self.comboBox_device_list.setSizePolicy(sizePolicy)

        self.horizontalLayout_device.addWidget(self.comboBox_device_list)

        self.verticalLayout_device_buttom = QVBoxLayout()
        self.verticalLayout_device_buttom.setObjectName(u"verticalLayout_device_buttom")
        self.pushButton_root = QPushButton(self.verticalLayoutWidget)
        self.pushButton_root.setObjectName(u"pushButton_root")

        self.verticalLayout_device_buttom.addWidget(self.pushButton_root)

        # self.pushButton_kill_cam = QPushButton(self.verticalLayoutWidget)
        # self.pushButton_kill_cam.setObjectName(u"pushButton_kill_cam")
        #
        # self.verticalLayout_device_buttom.addWidget(self.pushButton_kill_cam)


        self.horizontalLayout_device.addLayout(self.verticalLayout_device_buttom)


        self.verticalLayout_main.addLayout(self.horizontalLayout_device)

        self.tabWidget_main = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tab_log_level = QWidget()
        self.tab_log_level.setObjectName(u"tab_log_level")
        self.level_tab_frame = LogLevelTabFrame(LevelModule(), self.tab_log_level)
        self.level_tab_frame.setFrameShape(QFrame.StyledPanel)
        self.level_tab_frame.setFrameShadow(QFrame.Raised)
        self.tabWidget_main.addTab(self.tab_log_level, "")
        self.tabWidget_main.setCurrentWidget(self.tab_log_level)
        self.tab_log_pull = QWidget()
        self.tab_log_pull.setObjectName(u"tab_log_pull")
        settingModule = GeneralSettings()
        self.log_pull_frame = LogPullTabFrame(PullModule(settingModule), self.tab_log_pull)
        self.log_pull_frame.setFrameShape(QFrame.StyledPanel)
        self.log_pull_frame.setFrameShadow(QFrame.Raised)
        self.tabWidget_main.addTab(self.tab_log_pull, "")

        self.verticalLayout_main.addWidget(self.tabWidget_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, windowSize[0], 22))
        self.menu_setting = QMenu(self.menubar)
        self.menu_setting.setObjectName(u"menu_setting")
        self.menu_device = QMenu(self.menubar)
        self.menu_device.setObjectName(u"menu_device")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.addWidget(QLabel(GetVersionStr()), 1)
        self.__latestVersion = QLabel("")
        self.__latestVersion.setObjectName(u"LatestLabel")
        self.statusbar.addWidget(self.__latestVersion, 1)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_setting.menuAction())
        self.menubar.addAction(self.menu_device.menuAction())
        self.menu_setting.addAction(self.action_general_settings)
        self.menu_setting.addAction(self.action_log_level_settings)
        self.menu_setting.addSeparator()
        self.menu_setting.addAction(self.action_check_update)
        self.menu_device.addAction(self.action_refresh_device_list)

        # setup setting panels
        parsePanelSize = (windowSize[0] * 8 / 5, windowSize[1] / 2)
        self.__parserDialog = LogLevelParsePanel(self, parsePanelSize, LogLevelParser(self.level_tab_frame))
        self.__parserDialog.setupUi()
        self.__parserDialog.setWindowModality(Qt.ApplicationModal)

        generalSettingPanelSize = (windowSize[0] * 2 / 3, windowSize[1] / 3)
        self.__generalSettingDialog = GeneralSettingPanel(self, generalSettingPanelSize, settingModule)
        self.__generalSettingDialog.setupUi()
        self.__generalSettingDialog.setWindowModality(Qt.ApplicationModal)
        self.__autoUpdateDialog = UpdateDialog(self.__displaySize, self.__autoUpdateModule)

        self.retranslateUi(MainWindow)
        self.__connectUi()

        QMetaObject.connectSlotsByName(MainWindow)

        t = self.DeviceThread(self.__adbManager, self.comboBox_device_list, self.__onDeviceChanged, 0)
        t.start()
    # setupUi

    def show(self, isFirstTime):
        super().show()
        levelTabGeo = self.tab_log_level.geometry()
        statusBarSize = self.statusbar.size()
        self.level_tab_frame.setGeometry(QRect(0, 0, levelTabGeo.width(), levelTabGeo.height() - statusBarSize.height() - 10))
        self.level_tab_frame.layoutFrame()
        self.log_pull_frame.setGeometry(QRect(0, 0, levelTabGeo.width(), levelTabGeo.height() - statusBarSize.height() - 10))
        self.log_pull_frame.layoutFrame()
        if isFirstTime:
            self.__parserDialog.show()

        self.__isChecking = True
        self.__autoUpdateDialog.SetIsForce(False)
        self.__updateThread.start()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", TITLE_PREFIX, None))
        self.action_general_settings.setText(QCoreApplication.translate("MainWindow", u"\u901a\u7528\u8bbe\u7f6e", None))
        self.action_log_level_settings.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u6790log\u7b49\u7ea7\u8bbe\u7f6e", None))
        self.action_check_update.setText(QCoreApplication.translate("MainWindow", u"检查更新", None))
        self.action_refresh_device_list.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u8bbe\u5907\u5217\u8868", None))
        self.label_device.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u5217\u8868", None))
        self.pushButton_root.setText(QCoreApplication.translate("MainWindow", u"remount", None))
        # self.pushButton_kill_cam.setText(QCoreApplication.translate("MainWindow", u"kill Camera server", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_log_level), QCoreApplication.translate("MainWindow", u"log\u7b49\u7ea7\u8bbe\u7f6e", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_log_pull), QCoreApplication.translate("MainWindow", u"log\u62c9\u53d6", None))
        self.menu_setting.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.menu_device.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907", None))
    # retranslateUi

    def __connectUi(self):

        # menu
        self.action_log_level_settings.triggered.connect(self.__onMenu)
        self.action_general_settings.triggered.connect(self.__onMenu)
        self.action_check_update.triggered.connect(self.__onMenu)
        self.action_refresh_device_list.triggered.connect(self.__onMenu)

        self.__updateThread.versionChecked.connect(self.__onCheckUpdate)

        self.device_changed.connect(self.__onUSBStateChanged)

        self.pushButton_root.clicked.connect(self.__onRemount)

    def __onMenu(self):
        if self.sender() == self.action_log_level_settings:
            self.__parserDialog.show()
        elif self.sender() == self.action_general_settings:
            self.__generalSettingDialog.show()
        elif (self.sender() == self.action_check_update) and (not self.__isChecking):
            self.__isChecking = True
            self.__autoUpdateDialog.SetIsForce(True)
            self.__updateThread.SetIsForce(True)
            self.__updateThread.start()
        elif self.sender() == self.action_refresh_device_list:
            self.__updateDevice()

    def __updateDevice(self, delay=0):
        sleep(delay)

        self.__deviceInfo = self.__adbManager.GetDeviceInfo(True)
        self.comboBox_device_list.clear()
        if not self.__deviceInfo == None:
            infos = []
            for info in self.__deviceInfo:
                infoStr = " %s: %s \t [Status:%s]" % (info[DEVICE_INFO_NAME], info[DEVICE_INFO_ID], info[DEVICE_INFO_STATUS])
                infos.append(infoStr)
            self.comboBox_device_list.addItems(infos)
        self.__onDeviceChanged()

    def __onRemount(self):
        res = self.__adbManager.Remount()
        t, m = ErrorCodeToMessage(res)
        ShowMessageDialog(t, m)


    def __onDeviceChanged(self):
        currentSelected = self.comboBox_device_list.currentIndex()
        if currentSelected == -1:
            title = TITLE_PREFIX
        else:
            title = "%s - %s (%s)" % (TITLE_PREFIX, self.__deviceInfo[currentSelected][DEVICE_INFO_ID], self.__deviceInfo[currentSelected][DEVICE_INFO_STATUS])
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
            self.__autoUpdateDialog.show(latestVersion)
        self.__isChecking = False
        self.__latestVersion.setText("最新版本:%s" % latestVersion)
