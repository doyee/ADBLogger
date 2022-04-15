from module.sqlManager import SQLManager
from module.toolModule import ToolModule
from module.table import *

LOG_GROUPS = ["overrideLogLevels", "CamxLogDebug", "CamxLogError", "CamxLogWarning", "CamxLogConfig", "CamxLogInfo", "CamxLogVerbose", "CamxLogCoreCfg"]
OVERRIDE_LOG_MASK = ["Error", "Warning", "Config", "Info", "Dump", "Verbose", "Log", "Core Config"]

class LevelModule(ToolModule):

    def __init__(self):
        super().__init__()
        self.__camxLogMasks = None
        self.__selection = {}

    def Update(self):
        self.__camxLogMasks = self.__getMaskFromDb()
        self.__selection = {}
        pass

    def SelectGroup(self, group):
        if len(self.__selection) > 0 and group in self.__selection.keys():
            return False
        self.__selection[group] = 0
        return True

    def DropGroup(self, group):
        if len(self.__selection) == 0:
            return False
        if group in self.__selection:
            self.__selection.pop(group)
            return True
        else:
            return False

    def SelectMask(self, group, mask):
        self.__calculate(group, mask, False, group == LOG_GROUPS[0])

    def DropMask(self, group, mask):
        self.__calculate(group, mask, True, group == LOG_GROUPS[0])

    def GetGroups(self):
        return LOG_GROUPS

    def GetMasksForGroup(self, group):
        if group == LOG_GROUPS[0]:
            return OVERRIDE_LOG_MASK
        else:
            return self.__camxLogMasks[0]

    def GetSelected(self):
        selected = []
        for group in LOG_GROUPS:
            try:
                value = self.__selection[group]
                selected.append("%s=%#x" % (group, value))
            except:
                pass
        return selected


    def __getMaskFromDb(self):
        info = SQLManager.QueryInfo()
        info.Table = maskTable.Table
        info.Columns = [maskTable.Mask, maskTable.Value]
        cursor = self._qsl_manager.Select(info)
        if cursor is not None:
            masks = []
            values = []
            for row in cursor:
                masks.append(row[0])
                values.append(row[1])
            return masks, values
        return None

    def __calculate(self, group, mask, isDrop, isOverrideLog):
        value = self.__selection[group]
        if isOverrideLog:
            maskValue = OVERRIDE_LOG_MASK.index(mask)
        else:
            maskValue = self.__camxLogMasks[1][self.__camxLogMasks[0].index(mask)]
        if isDrop:
            value &= ~(1 << maskValue)
        else:
            value |= 1 << maskValue

        self.__selection[group] = value

