from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMessageBox
from utils.defines import *

def GetWindowSize():
    primScreen =  QApplication.primaryScreen()
    rect = primScreen.geometry()
    return rect.width(), rect.height()

def ShowMessageDialog(msgType, msg):
    if msgType == MESSAGE_TYPE_INFO:
        messageBox = QMessageBox(QMessageBox.Warning, "提示", msg)
        messageBox.addButton(u"完成", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_WARNING:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", msg)
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


