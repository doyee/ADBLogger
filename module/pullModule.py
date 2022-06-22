from module.sqlManager import SQLManager
from module.table import *
from module.settingDefines import *
from module.toolModule import ToolModule
import gzip
from re import *
from utils.Utils import *
from natsort import natsorted
import functools

LOG_PREFIX = "androidlog"
OUTPUT_PREFIX = "android_logs_"

DIR_PICKER_TYPE_LAST_SRC = 0
DIR_PICKER_TYPE_LAST_DST = 1
DIR_PICKER_TYPE_LAST_SAVING = 2

class PullModule(ToolModule):
    def __init__(self, settingModule):
        super().__init__()
        self.__settingModule = settingModule
        self.__loggingType = 1 << LoggingType.APP_LOG | 1 << LoggingType.RIL_LOG | 1 << LoggingType.EVENTS_LOG | 1 << LoggingType.KMSG_LOG

    def SetLoggingType(self, type):
        self.__loggingType = type

    def Pull(self, dst):
        src = ANDROID_LOGS_ROOT
        res = self._adb_manager.Pull(src, dst)
        return res

    # applogcat-log.I210.20220518-205252.gz
    # applogcat-log.I213.20220518-215049.gz
    def SortByTimestamp(self, a, b):
        time_pos = 2
        time_a = a.split(".")[time_pos] # time_a: 20220518-205252
        time_b = b.split(".")[time_pos] # time_b: 20220518-215049
        if time_a < time_b:
            return -1
        if time_a > time_b:
            return 1
        return 0

    def ShortcutMerge(self, src):
        return self.Merge(src, src)

    def __MergeByFilter(self, files, filter, src,dst):
        unordered_files = MatchFileNames(files, filter + ".*.gz")
        files = sorted(unordered_files,key=functools.cmp_to_key(self.SortByTimestamp))
        fileName = "%s_%d_merged.txt" % (filter, GetTimestamp())
        if files is None or len(files) == 0:
            return ERROR_CODE_EMPTY_LOG_DIR
        file = JoinPath(dst, fileName)
        f = open(file, "ab+")
        for gz in files:
            g_file = gzip.GzipFile(JoinPath(src, gz)).read()
            f.write(g_file)
            f.write(bytes("\n", encoding="utf8"))
        f.close()
        return ERROR_CODE_SUCCESS

    def Merge(self, src, dst):
        files = FindAllChildren(src)
        error = ERROR_CODE_EMPTY_LOG_DIR
        for logType, logFilter in LoggingDict.items():
            if self.__loggingType & 1 << logType:
                # one of logFilter merged success mean Merge function success.
                error *= self.__MergeByFilter(files,logFilter,src,dst)

        return error

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
