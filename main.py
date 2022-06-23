import os.path

from module.adbManager import *
from module.settingDefines import *
from module.shortcutModule import ShortcutModule
from module.sqlManager import *
from uilogic.mainWindow import MainWindow
from utils.UIUtils import *


def launchCheck():
    firstTimeFlag = False
    # 1. check adb
    hasAdb = ADBManager.get_instance().CheckADB()
    if not hasAdb:
        ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_ADB_ERROR_QUIT)
        sys.exit(0)

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
    if firstTimeFlag:
        Init_DB()
    return firstTimeFlag


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        shortcut = ShortcutModule()
        sys.exit(0)
    else:
        firstTime = launchCheck()
        window = MainWindow()
        window.show(firstTime)
        sys.exit(app.exec_())
