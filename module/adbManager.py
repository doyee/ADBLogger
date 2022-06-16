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

    def Remount(self):
        if self.__selectedDevice == -1:
            return ERROR_CODE_NO_DEVICE
        cmd = "%s -s %s root" % (self.__adbPath, self.GetSelectedDeviceId())
        IF_Print("cmd: %s" % cmd)
        res = RunCmdAndReturn(cmd)

        if res.count("production builds") > 0:
            return ERROR_CODE_PRODUCTION_DEVICE
        elif (res.__len__() > 0) and (res.count("already running as root") == 0):
            return ERROR_CODE_UNKNOWN

        cmd = "%s -s %s remount" % (self.__adbPath, self.GetSelectedDeviceId())
        IF_Print("cmd: %s" % cmd)
        res = RunCmdAndReturn(cmd)

        if res.count("Not running as root") > 0:
            return ERROR_CODE_REMOUNT_FAILED
        else:
            return ERROR_CODE_SUCCESS

    def KillCameraServer(self):
        if self.__selectedDevice == -1:
            return ERROR_CODE_NO_DEVICE
        cmd = "%s -s %s root" % (self.__adbPath, self.GetSelectedDeviceId())
        IF_Print("cmd: %s" % cmd)
        res = RunCmdAndReturn(cmd)
        IF_Print("RunCmdAndReturn: %s" % res)
        kill_cmd = "kill $( ps -e | grep -ie 'camera' | awk '{print $2}')"
        cmd = "%s wait-for-device shell \"%s\"  " % (self.__adbPath, kill_cmd)
        IF_Print("cmd: %s" % cmd)
        res = RunCmdAndReturn(cmd)
        IF_Print("cmd: %s" % res)
        return ERROR_CODE_SUCCESS


    def Mkdir(self, dir):
        if self.__selectedDevice == -1:
            return ERROR_CODE_NO_DEVICE
        cmd = "%s -s %s shell mkdir %s" % (self.__adbPath, self.GetSelectedDeviceId(), dir)
        IF_Print(cmd)
        result = RunCmdAndReturn(cmd)
        IF_Print(result)
        if result == "" or result.count("exists") > 0:
            return ERROR_CODE_SUCCESS
        else:
            return ERROR_CODE_ADB_MKDIR_FAILED

    def Pull(self, src, dest):
        if self.__selectedDevice == -1:
            return ERROR_CODE_NO_DEVICE
        cmd = "%s -s %s pull %s %s" % (self.__adbPath, self.GetSelectedDeviceId(), src, dest)
        IF_Print("cmd: %s" % cmd)
        result = RunCmdAndReturn(cmd)
        IF_Print(result)
        if (result.count("not exist") > 0) or (result.count("No such file or directory") > 0):
            return ERROR_CODE_ADB_PULL_NOT_EXIST
        elif result.count("adb: error:") > 0:
            return ERROR_CODE_ADB_PULL_FAILED
        return ERROR_CODE_SUCCESS

    def Push(self, src, dest):
        if self.__selectedDevice == -1:
            return ERROR_CODE_NO_DEVICE
        cmd = "%s -s %s push %s %s" % (self.__adbPath, self.GetSelectedDeviceId(), src, dest)
        IF_Print("cmd: %s" % cmd)
        result = RunCmdAndReturn(cmd)
        IF_Print(result)
        if result.count("adb: error:") > 0:
            return ERROR_CODE_ADB_PUSH_FAILED
        return ERROR_CODE_SUCCESS

    def GetSelectedDeviceId(self):
        if self.__selectedDevice == -1:
            return None
        else:
            return self.__deviceInfo[self.__selectedDevice][DEVICE_INFO_ID]

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


