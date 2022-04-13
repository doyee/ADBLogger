import os.path

from utils.Utils import *
import sqlite3
import threading, time

def IsDbExist(path):
    return os.path.exists(path)

class SQLManager(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.__db = None

    @classmethod
    def get_instance(cls):
        if not hasattr(SQLManager, '_instance'):
            with SQLManager._instance_lock:
                if not hasattr(SQLManager, '_instance'):
                    SQLManager._instance = SQLManager()

        return SQLManager._instance
