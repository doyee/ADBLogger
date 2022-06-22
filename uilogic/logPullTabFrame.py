from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui.LogPullMerger import Ui_LogPull as UILog
from module.pullModule import *
from utils.UIUtils import *


class LogPullTabFrame(QFrame, UILog):
    def __init__(self, module, parent=None):
        super().__init__(parent)
        self._module = module
        self.__workingType = 1 << WORKING_TYPE_PULL_AND_MERGE
        self.__loggingType = 1 << LoggingType.APP_LOG

    def buildUp(self):
        self.setupUi(self)
        self.__connectUi()
        self.__onTypeSelected()

    def __connectUi(self):
        self.radioButton_pull.clicked.connect(self.__onTypeSelected)
        self.radioButton_merge.clicked.connect(self.__onTypeSelected)
        self.checkBox_save_pull.clicked.connect(self.__onTypeSelected)

        self.pushButton_save_pull.clicked.connect(self.__onChooseDir)
        self.pushButton_src.clicked.connect(self.__onChooseDir)
        self.pushButton_dst.clicked.connect(self.__onChooseDir)

        self.pushButton_run.clicked.connect(self.__onWork)

    def __onTypeSelected(self):
        if self.radioButton_merge.isChecked():
            self.__workingType = 1 << WORKING_TYPE_MERGE
        else:
            self.__workingType = 1 << WORKING_TYPE_PULL_AND_MERGE

        if self.sender() == self.radioButton_pull:
            self.__workingType = 1 << WORKING_TYPE_PULL_AND_MERGE
            if self.checkBox_save_pull.isChecked():
                self.__workingType |= 1 << WORKING_TYPE_PULL_AND_SAVE
            else:
                self.__workingType &= ~(1 << WORKING_TYPE_PULL_AND_SAVE)
        elif self.sender() == self.radioButton_merge:
            self.__workingType = 1 << WORKING_TYPE_MERGE
        elif self.sender() == self.checkBox_save_pull:
            if self.checkBox_save_pull.isChecked():
                self.__workingType |= 1 << WORKING_TYPE_PULL_AND_SAVE
            else:
                self.__workingType &= ~(1 << WORKING_TYPE_PULL_AND_SAVE)
        IF_Print("onTypeSelected: ", self.__workingType)
        self.__updateUIForWorkingType()

    def __updateUIForWorkingType(self):
        self.checkBox_save_pull.setEnabled(self.__workingType & 1 << WORKING_TYPE_PULL_AND_MERGE)
        self.label_save_pull.setEnabled(self.__workingType & 1 << WORKING_TYPE_PULL_AND_MERGE)
        self.lineEdit_save_pull.setEnabled(self.__workingType & 1 << WORKING_TYPE_PULL_AND_SAVE)
        self.pushButton_save_pull.setEnabled(self.__workingType & 1 << WORKING_TYPE_PULL_AND_SAVE)
        self.lineEdit_src.setEnabled(self.__workingType & 1 << WORKING_TYPE_MERGE)
        self.pushButton_src.setEnabled(self.__workingType & 1 << WORKING_TYPE_MERGE)

        if self.__workingType & 1 << WORKING_TYPE_PULL_AND_MERGE:
            self.pushButton_run.setText(QCoreApplication.translate("TabFrame", u"拉取并合并", None))
        elif self.__workingType & 1 << WORKING_TYPE_MERGE:
            self.pushButton_run.setText(QCoreApplication.translate("TabFrame", u"开始合并", None))

    def __onChooseDir(self):
        if self.sender() == self.pushButton_src:
            dir = self.__showDirPicker(DIR_PICKER_TYPE_LAST_SRC)
            if not dir == "":
                self.lineEdit_src.setText(dir)
        elif self.sender() == self.pushButton_dst:
            dir = self.__showDirPicker(DIR_PICKER_TYPE_LAST_DST)
            if not dir == "":
                self.lineEdit_dst.setText(dir)
        elif self.sender() == self.pushButton_save_pull:
            dir = self.__showDirPicker(DIR_PICKER_TYPE_LAST_SAVING)
            if not dir == "":
                self.lineEdit_save_pull.setText(dir)

    def __showDirPicker(self, type):
        lastPath = self._module.GetLastSelectedDir(type)
        dir = QFileDialog.getExistingDirectory(self,
                                               "请选择目录",
                                               lastPath)
        if not dir == "":
            self._module.UpdateLastSelectedDir(dir, type)
        return dir

    def __onWork(self):
        # check loggingType selected
        if self.checkBox_applogcat.isChecked():
            self.__loggingType |= 1 << LoggingType.APP_LOG
        if self.checkBox_eventlogcat.isChecked():
            self.__loggingType |= 1 << LoggingType.EVENTS_LOG
        if self.checkBox_kmsgcat.isChecked():
            self.__loggingType |= 1 << LoggingType.KMSG_LOG
        if self.checkBox_rillogcat.isChecked():
            self.__loggingType |= 1 << LoggingType.RIL_LOG

        self._module.SetLoggingType(self.__loggingType)

        if self.lineEdit_dst.text() == "":
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_MERGE_DST_EMPTY)
            return
        src = ""
        dst = self.lineEdit_dst.text()

        # check if pull
        if self.__workingType & 1 << WORKING_TYPE_PULL_AND_MERGE:
            # check if save
            if self.__workingType & 1 << WORKING_TYPE_PULL_AND_SAVE:
                if self.lineEdit_save_pull.text() == "":
                    ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_SAVE_DIR_EMPTY)
                else:
                    src = self.lineEdit_save_pull.text()
            else:
                src = dst
            # pull
            res = self._module.Pull(src)
            if not res == ERROR_CODE_SUCCESS:
                type, msg = ErrorCodeToMessage(res)
                ShowMessageDialog(type, msg)
                return
            src = JoinPath(src, "android_logs")
        elif self.__workingType & 1 << WORKING_TYPE_MERGE:
            # check src dir
            if self.lineEdit_src.text() == "":
                ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_SRC_DIR_EMPTY)
            else:
                src = self.lineEdit_src.text()

        # merge
        res = self._module.Merge(src, dst)
        t, m = ErrorCodeToMessage(res)
        ShowMessageDialog(t, m)
