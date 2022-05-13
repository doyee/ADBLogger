import os.path

import module
from utils.Utils import *
from utils.defines import *
import sqlite3
import threading, time
from module.table import *


def IsDbExist(path):
    return os.path.exists(path)

class SQLManager(object):
    _instance_lock = threading.Lock()

    class InsertInfo(object):
        Table = ""
        Headers = []
        Values = []
        isChar = []

    class QueryInfo(object):
        Table = ""
        Columns = []
        Conditions = ""

    class UpdateInfo(object):
        Table = ""
        Columns = []
        Values = []
        isChar = []
        Conditions = ""

    def __init__(self):
        path = os.path.join(os.path.join(GetAppDataDir(), TOOLS_ROOT_DIR), TOOLS_DB_MANE)
        self.__db = sqlite3.connect(path, check_same_thread=False)
        self.__checkDBUpdates()

    @classmethod
    def get_instance(cls):
        if not hasattr(SQLManager, '_instance'):
            with SQLManager._instance_lock:
                if not hasattr(SQLManager, '_instance'):
                    SQLManager._instance = SQLManager()

        return SQLManager._instance

    def CreateTable(self, tableObj:table):
        query = tableObj.create()
        try:
            self.__db.cursor().execute(query)
            self.__db.commit()
            return True
        except:
            print("cannot create EXISTED table %s:\n%s" % (tableObj.Table, tableObj.create()))
            return False

    def DeleteTable(self, tableObj:table):
        query = tableObj.delete()
        try:
            self.__db.cursor().execute(query)
            self.__db.commit()
        except:
            print("cannot delete table %s", tableObj.Table)


    def Insert(self, info:InsertInfo):
        query = """INSERT INTO %s (""" % info.Table
        for header in info.Headers:
            query += "%s," % header
        query = query[:-1] + ") VALUES ("
        for i in range(len(info.Values)):
            if info.isChar[i]:
                query += "\"%s\"," % info.Values[i]
            else:
                query += "%s," % info.Values[i]
        query = query[:-1] + ");"
        IF_Print(query)
        try:
            self.__db.cursor().execute(query)
            self.__db.commit()
            return ERROR_CODE_SUCCESS
        except Exception as e:
            print("insertion error: %s\n%s" % (query, e))
            return ERROR_CODE_DB_INSERT_FAILED

    def Select(self, info:QueryInfo):
        query = """SELECT """
        if len(info.Columns) == 0:
            query += "* FROM %s" % info.Table
        else:
            for clm in info.Columns:
                query += "%s," % clm
            query = query[:-1] + " FROM %s" % info.Table
        if not info.Conditions == "":
            query += " WHERE %s;" % info.Conditions
        else:
            query += ";"
        IF_Print(query)
        try:
            cursor = self.__db.cursor().execute(query)
            return cursor
        except Exception as e:
            print("cannot do query %s \n%s" % (query, e))
            return None

    def Update(self, info:UpdateInfo):
        query = """UPDATE %s SET""" % info.Table
        for i in range(len(info.Columns)):
            query = "%s %s=%s," % (query, info.Columns[i], str(info.Values[i]) if not info.isChar[i] else "\"%s\"" % str(info.Values[i]))
        query = "%s WHERE %s;" % (query[:-1], info.Conditions)
        IF_Print(query)
        try:
           self.__db.cursor().execute(query)
           self.__db.commit()
        except:
            print("cannot do query %s" % query)

    def __checkDBUpdates(self):
        query = """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s';""" % settingTable.Table
        count = self.__db.execute(query).fetchall()[0][0]
        if count == 0:
            return
        info = self.QueryInfo()
        info.Table = settingTable.Table
        info.Columns = [settingTable.Value]
        info.Conditions = "%s='%s'" % (settingTable.Name, module.settingDefines.SETTING_DB_VERSION)
        result = self.Select(info).fetchall()
        if len(result) == 0:
            querys = ["""PRAGMA foreign_keys = 0;""",
                      """CREATE TABLE sqlitestudio_temp_table AS SELECT * FROM SettingTable;""",
                      """DROP TABLE SettingTable;""",
                      """CREATE TABLE SettingTable (id INTEGER PRIMARY KEY NOT NULL, settingName TEXT NOT NULL, settingValue TEXT NOT NULL, settingType TEXT NOT NULL);""",
                      """INSERT INTO SettingTable (id, settingName, settingValue, settingType) SELECT id, settingName, settingValue, settingType FROM sqlitestudio_temp_table;""",
                      """DROP TABLE sqlitestudio_temp_table;""",
                      """PRAGMA foreign_keys = 1;"""]
            for q in querys:
                self.__db.execute(q)
            self.__db.commit()

            newInsert = [module.settingDefines.SETTING_DB_VERSION,
                         module.settingDefines.SETTING_IS_IGNORE_LATEST_UPDATE,
                         module.settingDefines.SETTING_LATEST_IGNORED_VERSION]
            for name in newInsert:
                insert = self.InsertInfo()
                insert.Table = settingTable.Table
                insert.Headers = settingTable.Headers[1:]
                insert.Values = [name, module.settingDefines.RUNTIME_SETTINGS_DEFAULT[name][0], module.settingDefines.RUNTIME_SETTINGS_DEFAULT[name][1]]
                insert.isChar = [True, True, True]
                self.Insert(insert)

        else:
            dbVersion = int(result[0][0])
            IF_Print("dbVersion:", dbVersion)
            # TO-DO: update tables in db as well as db version



