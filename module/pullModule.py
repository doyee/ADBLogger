from module.sqlManager import SQLManager
from module.table import *
from module.settingDefines import *
from module.toolModule import ToolModule
import gzip
from re import *
from utils.Utils import *
from natsort import natsorted

LOG_PREFIX = "androidlog"
OUTPUT_PREFIX = "android_logs_"

DIR_PICKER_TYPE_LAST_SRC = 0
DIR_PICKER_TYPE_LAST_DST = 1
DIR_PICKER_TYPE_LAST_SAVING = 2

class PullModule(ToolModule):
    def __init__(self, settingModule):
        super().__init__()
        self.__settingModule = settingModule

    def Pull(self, dst):
        src = ANDROID_LOGS_ROOT
        res = self._adb_manager.Pull(src, dst)
        return res

    def ShortcutMerge(self, src):
        files = FindAllChildren(src)
        files = natsorted(MatchFileNames(files, "androidlog.*.gz"))
        fileName = "%s%d_merged.txt" % (OUTPUT_PREFIX, GetTimestamp())
        if files is None or len(files) == 0:
            return ERROR_CODE_EMPTY_LOG_DIR
        file = JoinPath(src, fileName)
        f = open(file, "ab+")
        for gz in files:
            g_file = gzip.GzipFile(JoinPath(src, gz)).read()
            f.write(g_file)
            f.write(bytes("\n", encoding="utf8"))
        f.close()
        return ERROR_CODE_SUCCESS

    def Merge(self, src, dst):
        files = FindAllChildren(src)
        files = natsorted(MatchFileNames(files, "androidlog.*.gz"))
        fileName = "%s%d_merged.txt" % (OUTPUT_PREFIX, GetTimestamp())
        if files is None or len(files) == 0:
            return ERROR_CODE_EMPTY_LOG_DIR
        file = JoinPath(dst, fileName)
        f = open(file, "ab+")
        for gz in files:
            g_file = gzip.GzipFile(JoinPath(src, gz)).read()
            f.write(g_file)
            f.write(bytes("\n", encoding="utf8"))
        f.close()
        # TO-DO: check settings
        self.__settingModule.LoadSettings()
        if self.__settingModule.GetSetting(SETTING_OPEN_DIR):
            StartDir(dst)
        if self.__settingModule.GetSetting(SETTING_OPEN_FILE):
            exe = self.__settingModule.GetSetting(SETTING_OPEN_FILE_EXE)
            cmd = "\"%s\" \"%s\"" % (exe, file)
            RunCmdAsync(cmd)
        return ERROR_CODE_SUCCESS

    def GetLastSelectedDir(self, type):
        info = SQLManager.QueryInfo()
        info.Table = settingTable.Table
        info.Columns = [settingTable.Value]
        info.Conditions = "%s=\"%s\"" % (settingTable.Name, SETTING_LAST_SRC_DIR if type == DIR_PICKER_TYPE_LAST_SRC else SETTING_LAST_DEST_DIR if type == DIR_PICKER_TYPE_LAST_DST else SETTING_LAST_ADB_PULL_SAVE_DIR)
        return self._sql_manager.Select(info).fetchall()[0][0]

    def UpdateLastSelectedDir(self, dir, type):
        info = SQLManager.UpdateInfo()
        info.Table = settingTable.Table
        info.Columns = [settingTable.Value]
        info.Values = [dir]
        info.isChar = [True]
        info.Conditions =  "%s=\"%s\"" % (settingTable.Name, SETTING_LAST_SRC_DIR if type == DIR_PICKER_TYPE_LAST_SRC else SETTING_LAST_DEST_DIR if type == DIR_PICKER_TYPE_LAST_DST else SETTING_LAST_ADB_PULL_SAVE_DIR)
        self._sql_manager.Update(info)
