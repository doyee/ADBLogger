import sys, subprocess, os, time, threading
from utils.Utils import *
from utils.defines import *

class ADBManager(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.__adbPath = ""
        self.__deviceInfo = []
        self.__selectedDevice = -1
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
        if res.count("adb.exe") > 0:
            self.__adbPath = res[:-1]
            return True
        else:
            return False

    def GetDeviceInfo(self, refresh=False):
        if refresh:
            self.__deviceInfo = []
            self.__adbDevices()
        return self.__deviceInfo

    def SetSelectedDevice(self, index):
        self.__selectedDevice = index

    def __adbDevices(self):
        cmd = "%s devices" % self.__adbPath
        IF_Print("cmd: %s" % cmd)
        deviceList = RunCmdAndReturnList(cmd)[1:-1]
        self.__parseDeviceInfo(deviceList)

    def __parseDeviceInfo(self, deviceList):
        if len(deviceList) == 0:
            return None

        for deviceStr in deviceList:
            tmp = deviceStr.rsplit("\t")
            info = {}
            info[DEVICE_INFO_ID] = tmp[0]
            info[DEVICE_INFO_STATUS] = tmp[1]
            cmd = "%s -s %s shell getprop ro.product.model" % (self.__adbPath, tmp[0])
            IF_Print(cmd)
            name = RunCmdAndReturn(cmd)[:-2]
            if name.count("adb.exe") > 0:
                name = "UNKNOWN"
            info[DEVICE_INFO_NAME] = name
            self.__deviceInfo.append(info)


