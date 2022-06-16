# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogPullMerger.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogPull(object):
    def setupUi(self, LogPull):
        LogPull.setObjectName("LogPull")
        LogPull.resize(457, 393)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        LogPull.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(LogPull)
        self.gridLayout.setObjectName("gridLayout")
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridlayout.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.setObjectName("gridlayout")
        self.horizontalLayout_run = QtWidgets.QHBoxLayout()
        self.horizontalLayout_run.setObjectName("horizontalLayout_run")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_run.addItem(spacerItem)
        self.pushButton_run = QtWidgets.QPushButton(LogPull)
        self.pushButton_run.setObjectName("pushButton_run")
        self.horizontalLayout_run.addWidget(self.pushButton_run)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_run.addItem(spacerItem1)
        self.gridlayout.addLayout(self.horizontalLayout_run, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridlayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.horizontalLayout_type_select = QtWidgets.QHBoxLayout()
        self.horizontalLayout_type_select.setObjectName("horizontalLayout_type_select")
        self.radioButton_merge = QtWidgets.QRadioButton(LogPull)
        self.radioButton_merge.setChecked(True)
        self.radioButton_merge.setObjectName("radioButton_merge")
        self.horizontalLayout_type_select.addWidget(self.radioButton_merge)
        self.radioButton_pull = QtWidgets.QRadioButton(LogPull)
        self.radioButton_pull.setChecked(False)
        self.radioButton_pull.setObjectName("radioButton_pull")
        self.horizontalLayout_type_select.addWidget(self.radioButton_pull)
        self.gridlayout.addLayout(self.horizontalLayout_type_select, 1, 0, 1, 1)
        self.horizontalLayout_dst = QtWidgets.QHBoxLayout()
        self.horizontalLayout_dst.setObjectName("horizontalLayout_dst")
        self.lineEdit_dst = QtWidgets.QLineEdit(LogPull)
        self.lineEdit_dst.setObjectName("lineEdit_dst")
        self.horizontalLayout_dst.addWidget(self.lineEdit_dst)
        self.pushButton_dst = QtWidgets.QPushButton(LogPull)
        self.pushButton_dst.setObjectName("pushButton_dst")
        self.horizontalLayout_dst.addWidget(self.pushButton_dst)
        self.gridlayout.addLayout(self.horizontalLayout_dst, 6, 0, 1, 1)
        self.verticalLayout_save_pull = QtWidgets.QVBoxLayout()
        self.verticalLayout_save_pull.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_save_pull.setSpacing(6)
        self.verticalLayout_save_pull.setObjectName("verticalLayout_save_pull")
        self.checkBox_save_pull = QtWidgets.QCheckBox(LogPull)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_save_pull.sizePolicy().hasHeightForWidth())
        self.checkBox_save_pull.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_save_pull.setFont(font)
        self.checkBox_save_pull.setObjectName("checkBox_save_pull")
        self.verticalLayout_save_pull.addWidget(self.checkBox_save_pull)
        self.label_save_pull = QtWidgets.QLabel(LogPull)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_save_pull.sizePolicy().hasHeightForWidth())
        self.label_save_pull.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_save_pull.setFont(font)
        self.label_save_pull.setObjectName("label_save_pull")
        self.verticalLayout_save_pull.addWidget(self.label_save_pull)
        self.gridlayout.addLayout(self.verticalLayout_save_pull, 2, 0, 1, 1)
        self.horizontalLayout_src = QtWidgets.QHBoxLayout()
        self.horizontalLayout_src.setObjectName("horizontalLayout_src")
        self.lineEdit_src = QtWidgets.QLineEdit(LogPull)
        self.lineEdit_src.setObjectName("lineEdit_src")
        self.horizontalLayout_src.addWidget(self.lineEdit_src)
        self.pushButton_src = QtWidgets.QPushButton(LogPull)
        self.pushButton_src.setObjectName("pushButton_src")
        self.horizontalLayout_src.addWidget(self.pushButton_src)
        self.gridlayout.addLayout(self.horizontalLayout_src, 5, 0, 1, 1)
        self.horizontalLayout_save_pull = QtWidgets.QHBoxLayout()
        self.horizontalLayout_save_pull.setObjectName("horizontalLayout_save_pull")
        self.lineEdit_save_pull = QtWidgets.QLineEdit(LogPull)
        self.lineEdit_save_pull.setText("")
        self.lineEdit_save_pull.setObjectName("lineEdit_save_pull")
        self.horizontalLayout_save_pull.addWidget(self.lineEdit_save_pull)
        self.pushButton_save_pull = QtWidgets.QPushButton(LogPull)
        self.pushButton_save_pull.setObjectName("pushButton_save_pull")
        self.horizontalLayout_save_pull.addWidget(self.pushButton_save_pull)
        self.gridlayout.addLayout(self.horizontalLayout_save_pull, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.gridlayout, 0, 0, 1, 1)

        self.retranslateUi(LogPull)
        QtCore.QMetaObject.connectSlotsByName(LogPull)

    def retranslateUi(self, LogPull):
        _translate = QtCore.QCoreApplication.translate
        LogPull.setWindowTitle(_translate("LogPull", "日志合并"))
        self.pushButton_run.setText(_translate("LogPull", "拉取并合并"))
        self.radioButton_merge.setText(_translate("LogPull", "合并本地log"))
        self.radioButton_pull.setText(_translate("LogPull", "从设备拉取并合并"))
        self.lineEdit_dst.setPlaceholderText(_translate("LogPull", "选择/输入/拖入 合并log保存路径"))
        self.pushButton_dst.setText(_translate("LogPull", "选择目录"))
        self.checkBox_save_pull.setText(_translate("LogPull", "将拉取的log保存到指定目录"))
        self.label_save_pull.setText(_translate("LogPull", "若不指定，将保存在loig合并后输出的目录"))
        self.lineEdit_src.setPlaceholderText(_translate("LogPull", "选择/输入/拖入 本地log路径"))
        self.pushButton_src.setText(_translate("LogPull", "选择目录"))
        self.lineEdit_save_pull.setPlaceholderText(_translate("LogPull", "选择/输入/拖入 adb拉取保存目录"))
        self.pushButton_save_pull.setText(_translate("LogPull", "选择目录"))
