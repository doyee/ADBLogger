from module.sqlManager import SQLManager
from module.table import *
from module.settingDefines import *

from utils.Utils import *

class GeneralSettings(object):

    def __init__(self):
        self.__sql_manager = SQLManager.get_instance()
        self.__settings = {}

    def LoadSettings(self):
        for setting in GENERAL_SETTINGS_DEFAULT.keys():
            info = SQLManager.QueryInfo()
            info.Table = settingTable.Table
            info.Columns = [settingTable.Value, settingTable.Type]
            info.Conditions = "%s=\"%s\"" % (settingTable.Name, setting)
            result = self.__sql_manager.Select(info).fetchall()[0]
            self.__convert_result(setting, result)
        IF_Print("General Settings: %s " % self.__settings)
        return self.__settings

    def Reset(self):
        self.__settings = {}
        for setting in GENERAL_SETTINGS_DEFAULT.keys():
            self.__settings[setting] = GENERAL_SETTINGS_DEFAULT[setting][0]
        return self.__settings

    def GetSettings(self):
        return self.__settings

    def GetSetting(self, key):
        return self.__settings[key]

    def UpdataSettings(self, key, value):
        self.__settings[key] = value

    def Apply(self):
        for setting in self.__settings.keys():
            info = SQLManager.UpdateInfo()
            info.Table = settingTable.Table
            info.Columns = [settingTable.Value]
            info.Values = [self.__settings[setting]]
            info.isChar = [True]
            info.Conditions = "%s=\"%s\"" % (settingTable.Name, setting)
            self.__sql_manager.Update(info)

    def __convert_result(self, key, result):
        if result[0] == "None":
            self.__settings[key] = None
        else:
            if result[1] == settingTable.Type_Str:
                self.__settings[key] = result[0]
            elif result[1] == settingTable.Type_Bool:
                self.__settings[key] = True if result[0] == "True" else False



