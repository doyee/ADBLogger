from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
from utils.defines import *

def GetWindowSize():
    primScreen =  QApplication.primaryScreen()
    rect = primScreen.geometry()
    return rect.width(), rect.height()

def ShowMessageDialog(msgType, msg):
    if msgType == MESSAGE_TYPE_INFO:
        messageBox = QMessageBox(QMessageBox.Information, "提示", msg)
        messageBox.setWindowIcon(QIcon('icon/icon.resource'))
        messageBox.addButton(u"完成", QMessageBox.YesRole)
        messageBox.exec_()
    elif msgType == MESSAGE_TYPE_WARNING:
        messageBox = QMessageBox(QMessageBox.Warning, "警告", msg)
        messageBox.setWindowIcon(QIcon('icon/icon.resource'))
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

def PaintListViewSelectionBackground(model, index, color):
    item = model.itemFromIndex(index)
    item.setBackground(color)

def ListViewClickAllItem(listView):
    model = listView.model()
    rows = model.rowCount()
    for i in range(rows):
        index = model.index(i, 0)
        listView.clicked.emit(index)
        listView.setCurrentIndex(index)

def ListViewDoubleClickedAllItem(listView):
    model = listView.model()
    rows = model.rowCount()
    for i in range(rows):
        index = model.index(i, 0)
        listView.doubleClicked.emit(index)
        listView.setCurrentIndex(index)




