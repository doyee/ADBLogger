from module.sqlManager import SQLManager
from module.toolModule import ToolModule
from module.table import *

from utils.defines import *
from utils.Utils import *

LOG_GROUPS = ["overrideLogLevels", "CamxLogDebug", "CamxLogError", "CamxLogWarning", "CamxLogConfig", "CamxLogInfo", "CamxLogVerbose", "CamxLogCoreCfg"]
OVERRIDE_LOG_MASK = ["Error", "Warning", "Config", "Info", "Dump", "Verbose", "Log", "Core Config"]
LOG_MASK_ENABLE = [("System Log", True, "systemLogEnable"), ("Offline Log", False, "enableAsciiLogging"), ("DRQ Log", False, "logDRQEnable"), ("Metadata Log", False, "logMetaEnable")]
class LogMaskSelectionListener(object):
    @abstractmethod
    def onLogGroupSelectionChanged(self, isEmpty):
        pass

class LevelModule(ToolModule):

    def __init__(self):
        super().__init__()
        self.__camxLogMasks = None
        self.__enableMask = LOG_MASK_ENABLE.copy()
        self.__selection = {}
        self.__listener = None

    def SetListener(self, listener):
        self.__listener = listener

    def Update(self):
        self.__camxLogMasks = self.__getMaskFromDb()
        self.__selection = {}

    def GetEnableLogMasks(self):
        return self.__enableMask

    def UpdateEnableLogMask(self, mask: object, isEnable: object) -> object:
        for i in range(len(self.__enableMask)):
            if self.__enableMask[i][0] == mask:
                self.__enableMask[i] = mask, isEnable, self.__enableMask[i][2]
                break

    def ResetEnableLogMask(self):
        self.__enableMask = LOG_MASK_ENABLE.copy()
        return self.__enableMask

    def SelectGroup(self, group):
        if len(self.__selection) > 0 and group in self.__selection.keys():
            if self.__listener is not None:
                self.__listener.onLogGroupSelectionChanged(False)
            return False
        self.__selection[group] = []
        if self.__listener is not None:
            self.__listener.onLogGroupSelectionChanged(False)
        return True

    def DropGroup(self, group):
        if len(self.__selection) == 0:
            if self.__listener is not None:
                self.__listener.onLogGroupSelectionChanged(True)
            return False
        if group in self.__selection:
            self.__selection.pop(group)
            if self.__listener is not None:
                self.__listener.onLogGroupSelectionChanged(len(self.__selection) == 0)
            return True
        else:
            if self.__listener is not None:
                self.__listener.onLogGroupSelectionChanged(len(self.__selection) == 0)
            return False

    def SelectMask(self, group, mask):
        if len(self.__selection[group]) > 0 and mask in self.__selection[group]:
            return
        self.__selection[group].append(mask)

    def DropMask(self, group, mask):
        try:
            self.__selection[group].remove(mask)
        except:
            pass
        if self.__selection[group] == None:
            self.__selection[group] = []

    def GetGroups(self):
        return LOG_GROUPS

    def GetMasksForGroup(self, group):
        if group == LOG_GROUPS[0]:
            return OVERRIDE_LOG_MASK
        else:
            if self.__camxLogMasks is None:
                return None
            return self.__camxLogMasks[0]

    def GetSelectedMaskForGroup(self, group):
        return self.__selection[group]

    def GetSelected(self):
        selected = []
        for group in LOG_GROUPS:
            try:
                masks = self.__selection[group]
                selected.append("%s=%#x" % (group, self.__calculate(group == LOG_GROUPS[0], masks)))
            except:
                pass
        return selected

    def GetSelectedGroup(self, text):
        group = text[:text.find("=")]
        return LOG_GROUPS.index(group)

    def GetSelectedGroups(self):
        return self.__selection.keys()

    def SearchMask(self, group, mask):
        if group == LOG_GROUPS[0]:
            try:
                return OVERRIDE_LOG_MASK.index(mask)
            except:
                return -1
        else:
            try:
                return self.__camxLogMasks[0].index(mask)
            except:
                return -1

    def LoadSettingsFromFile(self, path=None):
        if path is not None:
            savingPath = path
        else:
            savingPath = JoinPath(JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR), CAMX_OVERRIDE_SETTINGS)
            res = self._adb_manager.Pull(CAMX_OVERRIDE_SETTINGS_PATH, savingPath)
            if not res == ERROR_CODE_SUCCESS:
                return res
        f = open(savingPath, "r+")
        loaded = self.__parseLogSettingsFile(f.readlines(), False)
        self.__selection = {}
        for line in loaded:
            setting = line.rsplit("=")
            try:
                if setting[0] in LOG_GROUPS:
                    bits = HexToBits(setting[1].replace("\n", ""))
                    self.__selection[setting[0]] = []
                    for bit in bits:
                        if setting[0] == LOG_GROUPS[0]:
                            self.__selection[setting[0]].append(OVERRIDE_LOG_MASK[bit])
                        else:
                            self.__selection[setting[0]].append(self.__camxLogMasks[0][bit])
                else:
                    for i in range(len(self.__enableMask)):
                        if setting[0] == self.__enableMask[i][2]:
                            value = True if setting[1].replace("\n", "").upper() == "TRUE" else False
                            self.__enableMask[i] = (self.__enableMask[i][0], value, self.__enableMask[i][2])
                            break
            except Exception as e:
                print(e)
                return ERROR_CODE_LOAD_LOG_LEVEL_SETTINGS_FAILED

        if loaded.__len__() <= 0:
            self.ResetEnableLogMask()
        IF_Print("log level selected: %s" % self.__selection)
        IF_Print("log level eneabled: %s" % self.__enableMask)
        return ERROR_CODE_SUCCESS

    def DropSettingsFromFile(self, path=None):
        if path is not None:
            savingPath = path
        else:
            savingPath = JoinPath(JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR), CAMX_OVERRIDE_SETTINGS)
            res = self._adb_manager.Pull(CAMX_OVERRIDE_SETTINGS_PATH, savingPath)
            if not res == ERROR_CODE_SUCCESS:
                return res
        f = open(savingPath, "r+")
        toWrite = self.__parseLogSettingsFile(f.readlines(), True)
        f.close()
        f = open(savingPath, "w+")
        f.writelines(toWrite)
        f.close()
        res = self._adb_manager.Push(savingPath, CAMX_OVERRIDE_SETTINGS_ROOT[:-1])
        return res

    def ApplySettings(self, path=None):
        res = self._adb_manager.Remount()
        if not res == ERROR_CODE_SUCCESS:
            return res
        if path is not None:
            savingPath = path
        else:
            savingPath = JoinPath(JoinPath(GetAppDataDir(), TOOLS_ROOT_DIR), CAMX_OVERRIDE_SETTINGS)
            res = self._adb_manager.Pull(CAMX_OVERRIDE_SETTINGS_PATH, savingPath)
        toWrite = []
        if res == ERROR_CODE_SUCCESS:
            f = open(savingPath, "r+")
            toWrite = self.__parseLogSettingsFile(f.readlines(), True)
            f.close()
        toWrite = toWrite + ConvertListToLines(self.GetSelected()) + ConvertListToLines(self.__getEnabledSettings())
        f = open(savingPath, "w+")
        f.writelines(toWrite)
        f.close()
        res = self._adb_manager.Mkdir(CAMX_OVERRIDE_SETTINGS_ROOT)
        if not res == ERROR_CODE_SUCCESS:
            return res
        res = self._adb_manager.Push(savingPath, CAMX_OVERRIDE_SETTINGS_ROOT[:-1])
        return res

    def __getEnabledSettings(self):
        enabled = []
        for enable in self.__enableMask:
            print(enable)
            enabled.append("%s=%s" % (enable[2], str(enable[1]).upper()))
        return enabled

    def __parseLogSettingsFile(self, lines, isExclude):
        toReturn = []
        for line in lines:
            flag = True
            for logMask in LOG_GROUPS:
                keyWord = logMask + "="
                if line.count(keyWord) > 0:
                    flag = False
                    break
            if not flag:
                if not isExclude:
                    toReturn.append(line)
                continue
            for des, value, logMask in LOG_MASK_ENABLE:
                keyWord = logMask + "="
                if line.count(keyWord) > 0:
                    flag = False
                    break
            if not flag:
                if not isExclude:
                    toReturn.append(line)
                continue
            elif isExclude:
                toReturn.append(line)
        return toReturn


    def __getMaskFromDb(self):
        info = SQLManager.QueryInfo()
        info.Table = maskTable.Table
        info.Columns = [maskTable.Mask, maskTable.Value]
        cursor = self._sql_manager.Select(info)
        if cursor is not None:
            masks = []
            values = []
            for row in cursor:
                masks.append(row[0])
                values.append(row[1])
            return masks, values
        return None

    def __calculate(self, isOverride, masks):
        value = 0
        for mask in masks:
            if isOverride:
                maskValue = OVERRIDE_LOG_MASK.index(mask)
            else:
                maskValue = self.__camxLogMasks[1][self.__camxLogMasks[0].index(mask)]
            value |= 1 << maskValue
        return value

