import pathlib
import sys

from PyQt5.QtWidgets import QWidget
from module.pullModule import PullModule
from utils.UIUtils import *
import argparse

SHORTCUT_OPT_MERGE = "M"


class ShortcutModule(object):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(description="adb tool shortcut")
        self.__parser.add_argument('-M', nargs=1, type=pathlib.Path)
        argvs = vars(self.__parser.parse_args(sys.argv[1:]))

        self.__handleOpt(argvs)

    def __handleOpt(self, argvs):
        mergePath = argvs[SHORTCUT_OPT_MERGE][0]
        errorCode = PullModule.ShortcutMerge(PullModule, mergePath)
        type, msg = ErrorCodeToMessage(errorCode)
        ShowMessageDialog(type, msg)
