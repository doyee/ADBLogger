import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui.mainWindow import MainWindow
from utils.Utils import *
from utils.defines import *
from utils.UIUtils import *
from module.sqlManager import *
from module.adbManager import *
from module.settingDefines import *

def launchCheck():
    firstTimeFlag = False
    # 1. check adb
    hasAdb = ADBManager.get_instance().CheckADB()
    if not hasAdb:
        ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_ADB_ERROR_QUIT)
        exit(0)

    # 2. check cache dir
    path = os.path.join(GetAppDataDir(), TOOLS_ROOT_DIR)
    if not IsPathExsist(path):
        Mkdir(path)
        firstTimeFlag = True
    else:
        # 3. check db
        path = os.path.join(path, TOOLS_DB_MANE)
        if not IsDbExist(path):
            firstTimeFlag = True
    # if firstTimeFlag:
    Init_DB()
    return firstTimeFlag

if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    firstTime = launchCheck()
    window = MainWindow()
    window.show(firstTime)
    sys.exit(app.exec_())