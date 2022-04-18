from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMessageBox
from utils.defines import *

def GetWindowSize():
    primScreen =  QApplication.primaryScreen()
    rect = primScreen.geometry()
    return rect.width(), rect.height()

def ShowMessageDialog(msgType):
    if msgType == MESSAGE_TYPE_SUCCESS:
        messageBox = QMessageBox(QMessageBox.Warning, "提示", "运行成功！")
        messageBox.addButton(u"完成", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_ADB_ERROR_QUIT:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "未找到有效的adb路径。请先将adb配置到PATH环境变量中。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_PARSER_EMPTY_INPUT:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "请输入有效的log等级定义。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_INVALID_PARAM:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "无效的输入。请检查后重新输入。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_DB_INSERT_FAILED:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "写入数据库失败。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_SEARCH_FAILED:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "没有找到匹配的项目。")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_NO_MASK:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", "没有找到对应的Mask值。请重新解析后再尝试。\n设置->解析log等级设置")
        messageBox.addButton(u"关闭", QMessageBox.YesRole)
        messageBox.exec_()

def FillupListView(parent, listView, data):
    model = QStandardItemModel(parent)
    for d in data:
        itm = QStandardItem(d)
        itm.setEditable(False)
        model.appendRow(itm)
    listView.setModel(model)

def FillupListViewWithHighlight(parent, listview, data, highlightIndex, color):
    model = QStandardItemModel(parent)
    for d in data:
        itm = QStandardItem(d)
        itm.setEditable(False)
        if d in highlightIndex:
            itm.setBackground(color)
        model.appendRow(itm)
    listview.setModel(model)

def PaintListViewSelectionBackground(listview, color):
    model = listview.model()
    index = listview.currentIndex()

    item = model.itemFromIndex(index)
    item.setBackground(color)


