from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from utils.defines import *

def GetWindowSize():
    primScreen =  QApplication.primaryScreen()
    rect = primScreen.geometry()
    return rect.width(), rect.height()

def ShowMessageDialog(msgType):
    if msgType == MESSAGE_TYPE_ADB_ERROR_QUIT:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "未找到有效的adb路径。请先将adb配置到PATH环境变量中。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()