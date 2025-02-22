from typing import Union

from PyQt5.QtGui import QColor
from enum import IntEnum


class LoggingType(IntEnum):
    APP_LOG = 1
    EVENTS_LOG = 2
    KMSG_LOG = 3
    RIL_LOG = 4


LoggingDict = {
    LoggingType.APP_LOG: "applogcat-log",
    LoggingType.EVENTS_LOG: "eventslogcat-log",
    LoggingType.KMSG_LOG: "kmsgcat-log",
    LoggingType.RIL_LOG: "rillogcat-log"
}

DEBUG = False
DEBUG_PRINT = True

# ERROR CODE
ERROR_CODE_BASE = 0
ERROR_CODE_SUCCESS = ERROR_CODE_BASE
ERROR_CODE_INVALID_PARAM = 1
ERROR_CODE_NO_DEVICE = 2
ERROR_CODE_ADB_PULL_FAILED = 3
ERROR_CODE_ADB_PULL_NOT_EXIST = 4
ERROR_CODE_ADB_PUSH_FAILED = 5
ERROR_CODE_ADB_MKDIR_FAILED = 6
ERROR_CODE_LOAD_LOG_LEVEL_SETTINGS_FAILED = 7
ERROR_CODE_EMPTY_LOG_DIR = 8
ERROR_CODE_PRODUCTION_DEVICE = 9
ERROR_CODE_REMOUNT_FAILED = 10
ERROR_CODE_DB_INSERT_FAILED = 11

ERROR_CODE_UNKNOWN = 1000

# MESSAGE TYPE
MESSAGE_TYPE_INFO = 0
MESSAGE_TYPE_WARNING = 1

MESSAGE_STR_SUCCESS = "运行成功！"
MESSAGE_STR_SETTINGS_APPLIED = "设置已生效。"
MESSAGE_STR_ADB_ERROR_QUIT = "未找到有效的adb路径。请先将adb配置到PATH环境变量中。"
MESSAGE_STR_PARSER_EMPTY_INPUT = "请输入有效的log等级定义。"
MESSAGE_STR_INVALID_PARAM = "无效的输入。请检查后重新输入。"
MESSAGE_STR_DB_INSERT_FAILED = "写入数据库失败。"
MESSAGE_STR_SEARCH_FAILED = "没有找到匹配的项目。"
MESSAGE_STR_NO_MASK = "没有找到对应的Mask值。请重新解析后再尝试。\n设置->解析log等级设置"
MESSAGE_STR_NO_DEVICE = "没有找到已连接的设备。请先连接设备，再做尝试。"
MESSAGE_STR_ADB_PULL_FAILED = "从设备中拉去失败。请检查：\n    1.设备是否连接\n    2.设备连接状态\n    3.设备是否ROOT\n    4.设备内是否存在对应文件"
MESSAGE_STR_ADB_PUSH_FAILED = "向设备中Push文件失败。请检查：\n    1.设备是否连接\n    2.设备连接状态\n    3.设备是否ROOT\n    4.设备内是否存在对应路径"
MESSAGE_STR_LOG_LEVEL_LOAD_FAILED = "导入设备中的log等级设置失败，请检查：\n    1.设备中的设置文件是否有效\n    2.解析的log等级是否和设备的log等级匹配"
MESSAGE_STR_SRC_DIR_EMPTY = "无效的路径。请检查所选择的路径。"
MESSAGE_STR_SAVE_DIR_EMPTY = "无效的保存路径。请检查从设备拉取的保存路径。"
MESSAGE_STR_MERGE_DST_EMPTY = "无效的输出路径。请检查合并后log输出的路径。"
MESSAGE_STR_EMPTY_LOG_DIR = "请选择有含有androidlog .gz的目录。"
MESSAGE_STR_PRODUCTION_DEVICE = "该设备为商用设备，无法Root。"
MESSAGE_STR_REMOUNT_FAILED = "Remount失败。"
MESSAGE_STR_NETWORK_ERROR = "网络连接失败，请重新尝试。"
MESSAGE_STR_DOWNLOAD_DONE_AND_INSTALL = "下载完成，关闭对话框开始自动安装。"
MESSAGE_STR_UNKNOWN_ERROR = "未知错误。"

WORKING_TYPE_PULL_AND_MERGE = 0
WORKING_TYPE_MERGE = 1
WORKING_TYPE_PULL_AND_SAVE = 2

WINDOWS = "windows"
MAC = "macOS"
LINUX = "linux"
SYSTEM = WINDOWS
RUNNABLE_WIN = ".exe"
RUNNABLE_MAC = ".dmg"
RUNNABLE_LINUX = ".deb"

UI_VERSION = "1.1"
MODULE_VERSION = "1.1"
DB_VERSION = 1
VERSION = "1.1"

DEVICE_INFO_ID = "deviceId"
DEVICE_INFO_NAME = "deviceName"
DEVICE_INFO_STATUS = "deviceStatus"

if not DEBUG:
    CAMX_OVERRIDE_SETTINGS_ROOT = "/vendor/etc/camera/"
    CAMX_OVERRIDE_SETTINGS = "camxoverridesettings.txt"
    ANDROID_LOGS_ROOT = "/data/log/android_logs"
else:
    CAMX_OVERRIDE_SETTINGS_ROOT = "/storage/emulated/0/test/"
    CAMX_OVERRIDE_SETTINGS = "test.txt"
    ANDROID_LOGS_ROOT = "/storage/emulated/0/test/android_logs"
CAMX_OVERRIDE_SETTINGS_PATH = CAMX_OVERRIDE_SETTINGS_ROOT + CAMX_OVERRIDE_SETTINGS

GIT_ACCOUNT = "doyee"
GIT_REPO = "AndroidLogs"

TOOLS_ROOT_DIR = "adbTools"
TOOLS_DB_NAME = "adbTools.db"

LIST_SELECTED_COLOR: Union[QColor, QColor] = QColor(0, 0, 255, 100)
LIST_NORMAL_COLOR = QColor(255, 255, 255, 255)


def ErrorCodeToMessage(errorCode):
    if errorCode == ERROR_CODE_SUCCESS:
        return MESSAGE_TYPE_INFO, MESSAGE_STR_SUCCESS
    elif errorCode == ERROR_CODE_NO_DEVICE:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_NO_DEVICE
    elif errorCode == ERROR_CODE_ADB_PULL_FAILED or errorCode == ERROR_CODE_ADB_PULL_NOT_EXIST:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_ADB_PULL_FAILED
    elif errorCode == ERROR_CODE_ADB_PUSH_FAILED:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_ADB_PUSH_FAILED
    elif errorCode == ERROR_CODE_LOAD_LOG_LEVEL_SETTINGS_FAILED:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_LOG_LEVEL_LOAD_FAILED
    elif errorCode == ERROR_CODE_EMPTY_LOG_DIR:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_EMPTY_LOG_DIR
    elif errorCode == ERROR_CODE_PRODUCTION_DEVICE:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_PRODUCTION_DEVICE
    elif errorCode == ERROR_CODE_REMOUNT_FAILED:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_REMOUNT_FAILED
    else:
        return MESSAGE_TYPE_WARNING, MESSAGE_STR_UNKNOWN_ERROR
