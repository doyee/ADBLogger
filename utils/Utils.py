import io, os
import time

from utils.defines import *
import subprocess, re

def IF_Print(*args, sep=' ', end='\n', file=None):
    if DEBUG_PRINT:
        print(*args, sep=' ', end='\n', file=None)

def GetVersionStr():
    return "Version[UI:%s  Mod:%s  db:%d]" % (UI_VERSION, MODULE_VERSION, DB_VERSION)

def StartDir(dir):
    os.startfile(dir)

def RunCmdAsync(cmd):
    os.popen(cmd)

def RunCmdSync(cmd):
    os.system(cmd)

def RunCmdAndReturn(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            bufsize=0,
                            start_new_session=True,
                            close_fds=True)
    result = io.TextIOWrapper(proc.stdout).read()
    return result

def RunCmdAndReturnList(cmd):
    result = os.popen(cmd)
    return result.read().splitlines()

def IsPathExsist(path):
    return os.path.exists(path)

def GetHome():
    return os.path.expanduser("~")

def GetDesktop():
    return os.path.join(GetHome(), "Desktop")

def GetAppDataDir():
    return os.getenv('APPDATA')

def Mkdir(path):
    try:
        os.mkdir(path)
    except:
        print("mkdir failed")
        return False
    return True

def JoinPath(parent, child):
    return os.path.join(parent, child)

def FindAllChildren(path):
    for dirpath, dirnames, filenames in os.walk(path):
        return filenames

def MatchFileNames(files, regExp):
    list = []
    for file in files:
        find = re.match(regExp, file)
        if find is not None:
            list.append(file)
    return list


def ConvertToHex(str):
    return int(str, 16)

def HexToBits(hex):
    value = int(bin(int(hex, 16)), 2)
    bits = []
    i = 0
    while value > 0:
        if 1 & value > 0:
            bits.append(i)
        i += 1
        value = value >> 1
    return bits

def ConvertListToLines(list):
    toReturn = []
    if len(list) > 0:
        for element in list:
            toReturn.append( str(element) + "\n")
    return toReturn

def GetTimestamp():
    return int(time.time()*1000)
