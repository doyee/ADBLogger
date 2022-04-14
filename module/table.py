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

tables = []