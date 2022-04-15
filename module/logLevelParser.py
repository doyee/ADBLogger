from utils.defines import *
from utils.Utils import *
from module.sqlManager import *
from module.table import *

class LogLevelParser(object):
    def __init__(self, listener):
        self.__mask = {}
        self.__sqlManager = SQLManager.get_instance()
        self.__parserListener = listener
        pass

    def Parse(self, str):
        self.__mask = {}
        definitions = []
        lines = str.rsplit("\n")
        for line in lines:
            lineEnd = line.find(";")
            if lineEnd > 0:
                define = line[:lineEnd]
                # 1. find assignment
                # [DEF, VAL]
                # we may have a case that xxx = xxx, so that we will get
                # [DEF, DEFINED_VAR]
                l_def = define.rsplit("=")
                # 2. parse definition
                l_define = l_def[0].rsplit(" ")
                definition = l_define[3].replace(" ", "")
                # 3. parse value
                if not l_def[1].find("CamxLogGroup") == -1:
                    # we are in special case
                    var = l_def[1][l_def[1].find("CamxLogGroup"):]
                    if var.find(" "):
                        var = var.replace(" ", "")
                    self.__mask[definition] = self.__mask[var]
                    definitions.append(definition)
                else:
                    s_val = l_def[1][l_def[1].find("<<") + 2:]
                    s_val = s_val.replace(" ", "")
                    if s_val == "":
                        return ERROR_CODE_INVALID_PARAM
                    val = ""
                    for char in s_val:
                        if char.isdigit():
                            val += char
                    self.__mask[definition] = int(val)
                    definitions.append(definition)

            elif line == "":
                continue
            else:
                return ERROR_CODE_INVALID_PARAM

        IF_Print(self.__mask)
        # 4. store the result into db
        t = maskTable()
        self.__sqlManager.DeleteTable(t)
        self.__sqlManager.CreateTable(t)
        if len(definitions) == 0:
            return ERROR_CODE_INVALID_PARAM

        idx = 0
        for define in definitions:
            insertInfo = SQLManager.InsertInfo()
            insertInfo.Table = maskTable.Table
            insertInfo.Headers = maskTable.Headers
            insertInfo.Values = [idx, define, self.__mask[define]]
            insertInfo.isChar = [False, True, False]
            idx += 1
            if self.__sqlManager.Insert(insertInfo) == ERROR_CODE_DB_INSERT_FAILED:
                return ERROR_CODE_DB_INSERT_FAILED
        self.__parserListener.onParseSuccess()
        return ERROR_CODE_SUCCESS

