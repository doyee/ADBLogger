from module.sqlManager import *
from module.adbManager import *

class ToolModule(object):
    def __init__(self):
        # TO-DO
        self._qsl_manager = SQLManager.get_instance()
        self._adb_manager = ADBManager.get_instance()