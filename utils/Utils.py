from utils.defines import *

UI_VERSION = "1.0.0.0"
MODULE_VERSION = "1.0.0.0"
DB_VERSION = 1

def IF_Print(*args, sep=' ', end='\n', file=None):
    if DEBUG_PRINT:
        print(*args, sep=' ', end='\n', file=None)

def GetVersionStr():
    return "Version[UI:%s  Mod:%s  db:%d]" % (UI_VERSION, MODULE_VERSION, DB_VERSION)