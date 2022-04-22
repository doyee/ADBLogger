import os.path

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
        self.__db = sqlite3.connect(path)

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
        except:
            print("insertion error: %s" % query)
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
        except:
            print("cannot do query %s" % query)
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
