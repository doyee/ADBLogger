from utils.Utils import *
from module.table import *
from module.sqlManager import SQLManager

SETTING_OPEN_DIR = "OpenDir"
SETTING_OPEN_FILE = "OpenFile"
SETTING_OPEN_FILE_EXE = "OpenFileExe"
SETTING_LAST_DEST_DIR = "LastDest"
SETTING_LAST_SRC_DIR = "LastSrc"
SETTING_LAST_ADB_PULL_SAVE_DIR = "LastPullSave"

GENERAL_SETTINGS_DEFAULT = {SETTING_OPEN_FILE: (False, settingTable.Type_Bool),
                            SETTING_OPEN_FILE_EXE: (None, settingTable.Type_Str),
                            SETTING_OPEN_DIR: (True, settingTable.Type_Bool)}

RUNTIME_SETTINGS_DEFAULT = {SETTING_LAST_DEST_DIR: (GetDesktop(), settingTable.Type_Str),
                            SETTING_LAST_SRC_DIR: (GetDesktop(), settingTable.Type_Str),
                            SETTING_LAST_ADB_PULL_SAVE_DIR: (GetDesktop(), settingTable.Type_Str)}


def Init_DB():
    table = settingTable()
    sql = SQLManager.get_instance()
    created = sql.CreateTable(table)
    if created:
        idx = 0
        for setting in GENERAL_SETTINGS_DEFAULT.keys():
            info = SQLManager.InsertInfo()
            info.Table = table.Table
            info.Headers = table.Headers
            info.Values = [idx, setting, GENERAL_SETTINGS_DEFAULT[setting][0], GENERAL_SETTINGS_DEFAULT[setting][1]]
            info.isChar = [False, True, True, True]
            sql.Insert(info)
            idx += 1

        for setting in RUNTIME_SETTINGS_DEFAULT.keys():
            info = SQLManager.InsertInfo()
            info.Table = table.Table
            info.Headers = table.Headers
            info.Values = [idx, setting, RUNTIME_SETTINGS_DEFAULT[setting][0], RUNTIME_SETTINGS_DEFAULT[setting][1]]
            info.isChar = [False, True, True, True]
            sql.Insert(info)
            idx += 1