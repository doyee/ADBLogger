import sys,subprocess,os,time,threading
from utils.Utils import *

class ADBManager(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.__adbPath = ""
        pass

    @classmethod
    def get_instance(cls):
        if not hasattr(ADBManager, '_instance'):
            with ADBManager._instance_lock:
                if not hasattr(ADBManager, '_instance'):
                    ADBManager._instance = ADBManager()

        return ADBManager._instance

    def CheckADB(self):
        cmd = "where adb"
        res = RunCmdAndReturn(cmd)
        IF_Print(res)
        return res.count("adb.exe") > 0
