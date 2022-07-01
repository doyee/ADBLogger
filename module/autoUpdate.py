import sys

import requests, module

from PyQt5.QtCore import *
from utils.Utils import *

from module.sqlManager import SQLManager
from module.table import settingTable

TIMEOUT = 100 # sec
GIT_API_URL = "https://api.github.com/repos/%s/%s/releases/latest" % (GIT_ACCOUNT, GIT_REPO)


class DownloadThread(QThread):
    downloadStart = pyqtSignal()
    downloadDone = pyqtSignal(bool, str)

    def __init__(self, path, url, size, parent=None):
        super().__init__(parent)
        self.__path = path
        self.__url = url
        self.__size = size

    def run(self) -> None:
        try:
            resp = requests.get(self.__url, stream=True, timeout=TIMEOUT)
            total = int(resp.headers.get("content-length", 0))
            if not self.__size == total:
                IF_Print("network error: size not match [total:%d - content:%d]" % (self.__size, total))
                self.downloadDone.emit(False, "")
                return
            IF_Print("\nStart Download at %s" % self.__url)

            with open(self.__path, "wb") as fp:
                self.downloadStart.emit()

                for data in resp.iter_content(chunk_size=1024):
                    try:
                        fp.write(data)
                    except Exception as e:
                        IF_Print("\nwriting failed: %s %s" % (self.__path, e))
                        self.downloadDone.emit(False, "")

                fp.close()
                self.downloadDone.emit(True, self.__path)


        except:
            IF_Print("\nnetwork error: cannot GET from %s Timeout: %d sec" % (self.__url, TIMEOUT))
            self.downloadDone.emit(False, "")

class AutoUpdate(QObject):
    def __init__(self):
        super().__init__()
        self.__db = SQLManager.get_instance()
        self.__latestReleaseInfo = {}

    def CheckUpdate(self, isForce=False):
        try:
            self.__latestReleaseInfo = requests.get(url=GIT_API_URL).json()
            latestVersion = self.__latestReleaseInfo["tag_name"]
            isUpdate, latestVersion = self.__checkVersion(latestVersion, isForce)
            return isUpdate, latestVersion
        except:
            IF_Print("network error: cannot request %s" % GIT_API_URL)
            return False, VERSION

    def Download(self):
        name, url, size = self.__parseAssets(self.__latestReleaseInfo["assets"])
        path = JoinPath(JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR), name)
        return path, url, size

    def Install(self, path):
        IF_Print("Start to Install", path)
        os.popen("start %s " % path)
        sys.exit(0)

    def IgnoreVersion(self, version):
        queryInfo = SQLManager.UpdateInfo()
        queryInfo.Table = settingTable.Table
        queryInfo.Columns = [settingTable.Value]
        queryInfo.Values = [version]
        queryInfo.isChar = [True]
        queryInfo.Conditions = "%s='%s'" % (settingTable.Name, module.settingDefines.SETTING_LATEST_IGNORED_VERSION)
        self.__db.Update(queryInfo)

    def __checkVersion(self, version, isForce):
        v = re.findall("\d+.\d+", version)[0]
        currVersion = VERSION

        queryInfo = SQLManager.QueryInfo()
        queryInfo.Table = settingTable.Table
        queryInfo.Columns = [settingTable.Value]
        queryInfo.Conditions = "%s='%s'" % (settingTable.Name, module.settingDefines.SETTING_LATEST_IGNORED_VERSION)

        ignoredVersion = self.__db.Select(queryInfo).fetchall()[0][0]
        if ignoredVersion == v:
            if isForce:
                return True, v
            return False, v

        if v > currVersion:
            return True, v
        return False, v

    def __parseAssets(self, assetInfo):
        runnableSuffix = GetRunnableSuffix()
        for asset in assetInfo:
            if len(re.findall(".*%s" % runnableSuffix, asset["name"])) > 0:
                return asset["name"], asset["browser_download_url"], int(asset["size"])




