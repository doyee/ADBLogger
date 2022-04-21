from module.toolModule import ToolModule
import gzip
from re import *
from utils.Utils import *
from natsort import natsorted

LOG_PREFIX = "androidlog"
OUTPUT_PREFIX = "android_logs_"

class PullModule(ToolModule):
    def __init__(self):
        super().__init__()

    def Pull(self, dst):
        src = ANDROID_LOGS_ROOT
        res = self._adb_manager.Pull(src, dst)
        return res

    def Merge(self, src, dst):
        files = FindAllChildren(src)
        files = natsorted(MatchFileNames(files, "androidlog.*.gz"))
        fileName = "%s%d_merged.txt" % (OUTPUT_PREFIX, GetTimestamp())
        if files is None or len(files) == 0:
            return ERROR_CODE_EMPTY_LOG_DIR
        f = open(JoinPath(dst, fileName), "ab+")
        for gz in files:
            g_file = gzip.GzipFile(JoinPath(src, gz)).read()
            f.write(g_file)
            f.write(bytes("\n", encoding="utf8"))
        f.close()
        # TO-DO: check settings
        StartDir(dst)
        return ERROR_CODE_SUCCESS
