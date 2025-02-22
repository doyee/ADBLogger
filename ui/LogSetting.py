# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogSetting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogSetting(object):
    def setupUi(self, LogSetting):
        LogSetting.setObjectName("LogSetting")
        LogSetting.resize(509, 362)
        self.gridLayout = QtWidgets.QGridLayout(LogSetting)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_main = QtWidgets.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_settings = QtWidgets.QHBoxLayout()
        self.horizontalLayout_settings.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_settings.setSpacing(6)
        self.horizontalLayout_settings.setObjectName("horizontalLayout_settings")
        self.verticalLayout_group = QtWidgets.QVBoxLayout()
        self.verticalLayout_group.setObjectName("verticalLayout_group")
        self.horizontalLayout_group_heading = QtWidgets.QHBoxLayout()
        self.horizontalLayout_group_heading.setObjectName("horizontalLayout_group_heading")
        self.label_group = QtWidgets.QLabel(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_group.sizePolicy().hasHeightForWidth())
        self.label_group.setSizePolicy(sizePolicy)
        self.label_group.setObjectName("label_group")
        self.horizontalLayout_group_heading.addWidget(self.label_group)
        self.pushButton_group_reset = QtWidgets.QPushButton(LogSetting)
        self.pushButton_group_reset.setObjectName("pushButton_group_reset")
        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_reset)
        self.pushButton_group_select_all = QtWidgets.QPushButton(LogSetting)
        self.pushButton_group_select_all.setObjectName("pushButton_group_select_all")
        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_select_all)
        self.verticalLayout_group.addLayout(self.horizontalLayout_group_heading)
        self.label_current_group = QtWidgets.QLabel(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_current_group.sizePolicy().hasHeightForWidth())
        self.label_current_group.setSizePolicy(sizePolicy)
        self.label_current_group.setObjectName("label_current_group")
        self.verticalLayout_group.addWidget(self.label_current_group)
        self.listView_group = QtWidgets.QListView(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_group.sizePolicy().hasHeightForWidth())
        self.listView_group.setSizePolicy(sizePolicy)
        self.listView_group.setObjectName("listView_group")
        self.verticalLayout_group.addWidget(self.listView_group)
        self.horizontalLayout_settings.addLayout(self.verticalLayout_group)
        self.verticalLayout_mask = QtWidgets.QVBoxLayout()
        self.verticalLayout_mask.setObjectName("verticalLayout_mask")
        self.horizontalLayout_mask_heading = QtWidgets.QHBoxLayout()
        self.horizontalLayout_mask_heading.setObjectName("horizontalLayout_mask_heading")
        self.label_mask = QtWidgets.QLabel(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mask.sizePolicy().hasHeightForWidth())
        self.label_mask.setSizePolicy(sizePolicy)
        self.label_mask.setObjectName("label_mask")
        self.horizontalLayout_mask_heading.addWidget(self.label_mask)
        self.pushButton_mask_reset = QtWidgets.QPushButton(LogSetting)
        self.pushButton_mask_reset.setObjectName("pushButton_mask_reset")
        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_reset)
        self.pushButton_mask_select_all = QtWidgets.QPushButton(LogSetting)
        self.pushButton_mask_select_all.setObjectName("pushButton_mask_select_all")
        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_select_all)
        self.verticalLayout_mask.addLayout(self.horizontalLayout_mask_heading)
        self.horizontalLayout_search = QtWidgets.QHBoxLayout()
        self.horizontalLayout_search.setObjectName("horizontalLayout_search")
        self.lineEdit_mask_search = QtWidgets.QLineEdit(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_mask_search.sizePolicy().hasHeightForWidth())
        self.lineEdit_mask_search.setSizePolicy(sizePolicy)
        self.lineEdit_mask_search.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_mask_search.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_mask_search.setObjectName("lineEdit_mask_search")
        self.horizontalLayout_search.addWidget(self.lineEdit_mask_search)
        self.pushButton_mask_search = QtWidgets.QPushButton(LogSetting)
        self.pushButton_mask_search.setObjectName("pushButton_mask_search")
        self.horizontalLayout_search.addWidget(self.pushButton_mask_search)
        self.verticalLayout_mask.addLayout(self.horizontalLayout_search)
        self.listView_mask = QtWidgets.QListView(LogSetting)
        self.listView_mask.setObjectName("listView_mask")
        self.verticalLayout_mask.addWidget(self.listView_mask)
        self.horizontalLayout_settings.addLayout(self.verticalLayout_mask)
        self.verticalLayout_main.addLayout(self.horizontalLayout_settings)
        self.horizontalLayout_check = QtWidgets.QHBoxLayout()
        self.horizontalLayout_check.setObjectName("horizontalLayout_check")
        self.checkBox_systemlog = QtWidgets.QCheckBox(LogSetting)
        self.checkBox_systemlog.setObjectName("checkBox_systemlog")
        self.horizontalLayout_check.addWidget(self.checkBox_systemlog)
        self.checkBox_offlinelog = QtWidgets.QCheckBox(LogSetting)
        self.checkBox_offlinelog.setObjectName("checkBox_offlinelog")
        self.horizontalLayout_check.addWidget(self.checkBox_offlinelog)
        self.checkBox_drqlog = QtWidgets.QCheckBox(LogSetting)
        self.checkBox_drqlog.setObjectName("checkBox_drqlog")
        self.horizontalLayout_check.addWidget(self.checkBox_drqlog)
        self.checkBox_metadatalog = QtWidgets.QCheckBox(LogSetting)
        self.checkBox_metadatalog.setObjectName("checkBox_metadatalog")
        self.horizontalLayout_check.addWidget(self.checkBox_metadatalog)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_check.addItem(spacerItem)
        self.verticalLayout_main.addLayout(self.horizontalLayout_check)
        self.label_preview = QtWidgets.QLabel(LogSetting)
        self.label_preview.setObjectName("label_preview")
        self.verticalLayout_main.addWidget(self.label_preview)
        self.listView_preview = QtWidgets.QListView(LogSetting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_preview.sizePolicy().hasHeightForWidth())
        self.listView_preview.setSizePolicy(sizePolicy)
        self.listView_preview.setMaximumSize(QtCore.QSize(16777215, 120))
        self.listView_preview.setObjectName("listView_preview")
        self.verticalLayout_main.addWidget(self.listView_preview)
        self.horizontalLayout_buttons = QtWidgets.QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.pushButton_load = QtWidgets.QPushButton(LogSetting)
        self.pushButton_load.setObjectName("pushButton_load")
        self.horizontalLayout_buttons.addWidget(self.pushButton_load)
        self.pushButton_clear = QtWidgets.QPushButton(LogSetting)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout_buttons.addWidget(self.pushButton_clear)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_buttons.addItem(spacerItem1)
        self.pushButton_reset = QtWidgets.QPushButton(LogSetting)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout_buttons.addWidget(self.pushButton_reset)
        self.pushButton_apply = QtWidgets.QPushButton(LogSetting)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout_buttons.addWidget(self.pushButton_apply)
        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)
        self.gridLayout.addLayout(self.verticalLayout_main, 0, 0, 1, 1)

        self.retranslateUi(LogSetting)
        QtCore.QMetaObject.connectSlotsByName(LogSetting)

    def retranslateUi(self, LogSetting):
        _translate = QtCore.QCoreApplication.translate
        LogSetting.setWindowTitle(_translate("LogSetting", "日志开关"))
        self.label_group.setText(_translate("LogSetting", "Group"))
        self.pushButton_group_reset.setText(_translate("LogSetting", "重置"))
        self.pushButton_group_select_all.setText(_translate("LogSetting", "全选"))
        self.label_current_group.setText(_translate("LogSetting", "Current:"))
        self.label_mask.setText(_translate("LogSetting", "Mask"))
        self.pushButton_mask_reset.setText(_translate("LogSetting", "重置"))
        self.pushButton_mask_select_all.setText(_translate("LogSetting", "全选"))
        self.lineEdit_mask_search.setPlaceholderText(_translate("LogSetting", "请输入完整mask"))
        self.pushButton_mask_search.setText(_translate("LogSetting", "搜索"))
        self.checkBox_systemlog.setAccessibleName(_translate("LogSetting", "System Log"))
        self.checkBox_systemlog.setText(_translate("LogSetting", "System Log"))
        self.checkBox_offlinelog.setAccessibleName(_translate("LogSetting", "Offline Log"))
        self.checkBox_offlinelog.setText(_translate("LogSetting", "Offline Log"))
        self.checkBox_drqlog.setAccessibleName(_translate("LogSetting", "DRQ Log"))
        self.checkBox_drqlog.setText(_translate("LogSetting", "DRQ Log"))
        self.checkBox_metadatalog.setAccessibleName(_translate("LogSetting", "Metadata Log"))
        self.checkBox_metadatalog.setText(_translate("LogSetting", "Metadata Log"))
        self.label_preview.setText(_translate("LogSetting", "预览"))
        self.pushButton_load.setText(_translate("LogSetting", "读取设备预设"))
        self.pushButton_clear.setText(_translate("LogSetting", "清除设备预设"))
        self.pushButton_reset.setText(_translate("LogSetting", "恢复默认值"))
        self.pushButton_apply.setText(_translate("LogSetting", "应用"))
