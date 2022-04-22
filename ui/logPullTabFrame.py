from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.tabFrame import TabFrame
from ui.dropLineEditor import DropLineEditor
from utils.Utils import *
from utils.UIUtils import *
from utils.defines import *
from module.pullModule import *

class LogPullTabFrame(TabFrame):
    def __init__(self, module, parent=None):
        super().__init__(module, parent)
        self.__workingType = 1 << WORKING_TYPE_PULL_AND_MERGE

    def layoutFrame(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 10, 20, 10)
        self.horizontalLayout_type_select = QHBoxLayout()
        self.horizontalLayout_type_select.setObjectName(u"horizontalLayout_type_select")
        self.radioButton_pull = QRadioButton(self)
        self.radioButton_pull.setObjectName(u"radioButton_pull")
        self.radioButton_pull.setChecked(True)

        self.horizontalLayout_type_select.addWidget(self.radioButton_pull)

        self.radioButton_merge = QRadioButton(self)
        self.radioButton_merge.setObjectName(u"radioButton_merge")

        self.horizontalLayout_type_select.addWidget(self.radioButton_merge)


        self.verticalLayout.addLayout(self.horizontalLayout_type_select)

        self.verticalLayout_save_pull = QVBoxLayout()
        self.verticalLayout_save_pull.setSpacing(6)
        self.verticalLayout_save_pull.setObjectName(u"verticalLayout_save_pull")
        self.verticalLayout_save_pull.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.checkBox_save_pull = QCheckBox(self)
        self.checkBox_save_pull.setObjectName(u"checkBox_save_pull")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_save_pull.sizePolicy().hasHeightForWidth())
        self.checkBox_save_pull.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setWeight(50)
        self.checkBox_save_pull.setFont(font1)

        self.verticalLayout_save_pull.addWidget(self.checkBox_save_pull)

        self.label_save_pull = QLabel(self)
        self.label_save_pull.setObjectName(u"label_save_pull")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_save_pull.sizePolicy().hasHeightForWidth())
        self.label_save_pull.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setWeight(50)
        self.label_save_pull.setFont(font2)

        self.verticalLayout_save_pull.addWidget(self.label_save_pull)


        self.verticalLayout.addLayout(self.verticalLayout_save_pull)

        self.horizontalLayout_save_pull = QHBoxLayout()
        self.horizontalLayout_save_pull.setObjectName(u"horizontalLayout_save_pull")
        self.lineEdit_save_pull = DropLineEditor(self)
        self.lineEdit_save_pull.setObjectName(u"lineEdit_save_pull")
        self.lineEdit_save_pull.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_save_pull.addWidget(self.lineEdit_save_pull)

        self.pushButton_save_pull = QPushButton(self)
        self.pushButton_save_pull.setObjectName(u"pushButton_save_pull")

        self.horizontalLayout_save_pull.addWidget(self.pushButton_save_pull)


        self.verticalLayout.addLayout(self.horizontalLayout_save_pull)

        self.horizontalLayout_src = QHBoxLayout()
        self.horizontalLayout_src.setObjectName(u"horizontalLayout_src")
        self.lineEdit_src = DropLineEditor(self)
        self.lineEdit_src.setObjectName(u"lineEdit_src")
        self.lineEdit_src.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_src.addWidget(self.lineEdit_src)

        self.pushButton_src = QPushButton(self)
        self.pushButton_src.setObjectName(u"pushButton_src")

        self.horizontalLayout_src.addWidget(self.pushButton_src)


        self.verticalLayout.addLayout(self.horizontalLayout_src)

        self.horizontalLayout_dst = QHBoxLayout()
        self.horizontalLayout_dst.setObjectName(u"horizontalLayout_dst")
        self.lineEdit_dst = DropLineEditor(self)
        self.lineEdit_dst.setObjectName(u"lineEdit_dst")
        self.lineEdit_dst.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_dst.addWidget(self.lineEdit_dst)

        self.pushButton_dst = QPushButton(self)
        self.pushButton_dst.setObjectName(u"pushButton_dst")

        self.horizontalLayout_dst.addWidget(self.pushButton_dst)


        self.verticalLayout.addLayout(self.horizontalLayout_dst)

        self.horizontalLayout_run = QHBoxLayout()
        self.horizontalLayout_run.setObjectName(u"horizontalLayout_run")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_run.addItem(self.horizontalSpacer)

        self.pushButton_run = QPushButton(self)
        self.pushButton_run.setObjectName(u"pushButton_run")

        self.horizontalLayout_run.addWidget(self.pushButton_run)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_run.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_run)


        super().layoutFrame()
        self.__updateUIForWorkingType()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def _retranslateUi(self):
        self.radioButton_pull.setText(QCoreApplication.translate("TabFrame", u"\u4ece\u8bbe\u5907\u62c9\u53d6\u5e76\u5408\u5e76", None))
        self.radioButton_merge.setText(QCoreApplication.translate("TabFrame", u"\u5408\u5e76\u672c\u5730log", None))
        self.checkBox_save_pull.setText(QCoreApplication.translate("TabFrame", u"\u5c06\u62c9\u53d6\u7684log\u4fdd\u5b58\u5230\u6307\u5b9a\u76ee\u5f55", None))
        self.label_save_pull.setText(QCoreApplication.translate("TabFrame", u"\u82e5\u4e0d\u6307\u5b9a\uff0c\u5c06\u4fdd\u5b58\u5728log\u5408\u5e76\u540e\u8f93\u51fa\u7684\u76ee\u5f55", None))
        self.lineEdit_save_pull.setPlaceholderText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9/\u8f93\u5165/\u62d6\u5165 adb\u62c9\u53d6\u4fdd\u5b58\u76ee\u5f55", None))
        self.pushButton_save_pull.setText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9\u76ee\u5f55", None))
        self.lineEdit_src.setPlaceholderText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9/\u8f93\u5165/\u62d6\u5165 \u672c\u5730log\u8def\u5f84", None))
        self.pushButton_src.setText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9\u76ee\u5f55", None))
        self.lineEdit_dst.setPlaceholderText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9/\u8f93\u5165/\u62d6\u5165 \u5408\u5e76log\u4fdd\u5b58\u8def\u5f84", None))
        self.pushButton_dst.setText(QCoreApplication.translate("TabFrame", u"\u9009\u62e9\u76ee\u5f55", None))

    # retranslateUi

    def _connectUi(self):
        self.radioButton_pull.clicked.connect(self.__onTypeSelected)
        self.radioButton_merge.clicked.connect(self.__onTypeSelected)
        self.checkBox_save_pull.clicked.connect(self.__onTypeSelected)

        self.pushButton_save_pull.clicked.connect(self.__onChooseDir)
        self.pushButton_src.clicked.connect(self.__onChooseDir)
        self.pushButton_dst.clicked.connect(self.__onChooseDir)

        self.pushButton_run.clicked.connect(self.__onWork)

    def __onTypeSelected(self):
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
        if not res == ERROR_CODE_SUCCESS:
            t, m = ErrorCodeToMessage(res)
            ShowMessageDialog(t, m)
