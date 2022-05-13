from abc import abstractmethod

class table(object):
    Table = ""

    @abstractmethod
    def create(self):
        return ""

    @abstractmethod
    def delete(self):
        return ""

class maskTable(table):
    ## +--------------------------------------------------+
    ## | id (int prim) | maskName (str) | maskValue (int) |
    ## +--------------------------------------------------+
    Table = "MaskTabel"
    ID = "id"
    Mask = "maskName"
    Value = "maskValue"
    Headers = [ID, Mask, Value]

    def create(self):
        return """CREATE TABLE %s (%s INT PRIMARY KEY NOT NULL, %s TEXT NOT NULL, %s INT NOT NULL);""" % (self.Table, self.ID, self.Mask, self.Value)

    def delete(self):
        return "DROP TABLE IF EXISTS %s" % self.Table

class settingTable(table):
    ## +----------------------------------------------------------------------------+
    ## | id (int prim) | settingName (str) | settingValue (str) | settingType (str) |
    ## +----------------------------------------------------------------------------+

    Table = "SettingTable"
    ID = "id"
    Name = "settingName"
    Value = "settingValue"
    Type = "settingType"
    Type_Str = "String"
    Type_Int = "Int"
    Type_Float = "Float"
    Type_Bool = "BOOL"
    Headers = [ID, Name, Value, Type]

    def create(self):
        return """CREATE TABLE %s (%s INTEGER PRIMARY KEY NOT NULL, %s TEXT NOT NULL, %s TEXT NOT NULL, %s TEXT NOT NULL);""" % (self.Table, self.ID, self.Name, self.Value, self.Type)

tables = [settingTable()]