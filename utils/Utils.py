import io, os

from utils.defines import *
import subprocess

def IF_Print(*args, sep=' ', end='\n', file=None):
    if DEBUG_PRINT:
        print(*args, sep=' ', end='\n', file=None)

def GetVersionStr():
    return "Version[UI:%s  Mod:%s  db:%d]" % (UI_VERSION, MODULE_VERSION, DB_VERSION)

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

def GetAppDataDir():
    return os.getenv('APPDATA')

def Mkdir(path):
    try:
        os.mkdir(path)
    except:
        print("mkdir failed")
        return False
    return True