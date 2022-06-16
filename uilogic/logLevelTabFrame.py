from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller.logLevelParserListener import LogLevelParserListener
from module.levelModule import LogMaskSelectionListener
from utils.Utils import *
from utils.UIUtils import *
from ui.LogSetting import *

CURRENT_GROUP_PREFIX = u"Current:"

class LogLevelTabFrame(QFrame, Ui_LogSetting, LogLevelParserListener, LogMaskSelectionListener):

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.__checkBoxs = []
        self._module = module

    def buildUp(self):
        self.__setupUi()
        self.__connectUi()

    def __getCheckBoxByObjectName(self,name):
        object_name_checkbox = {
            "checkBox_systemlog": self.checkBox_systemlog,
            "checkBox_offlinelog": self.checkBox_offlinelog,
            "checkBox_drqlog": self.checkBox_drqlog,
            "checkBox_metadatalog": self.checkBox_metadatalog,
        }
        return object_name_checkbox.get(name,None)

    def __setupUi(self):
        self.setupUi(self)
        self.__fillMaskList()
        enableLogMask = self._module.GetEnableLogMasks()
        for i in range(len(enableLogMask)):
            des = enableLogMask[i][0]
            des = des.replace(" ", "").lower()
            object_name = "checkBox_%s" % des
            checkbox = self.__getCheckBoxByObjectName(object_name)
            checkbox.setChecked(enableLogMask[i][1])
            checkbox.clicked.connect(self.__onCheckBoxChecked)
            self.__checkBoxs.append(checkbox)

        self._module.SetListener(self)
        self._module.Update()
        self.__loadSettingFromFile()

    def __connectUi(self):
        self.pushButton_mask_search.clicked.connect(self.__onSearch)
        self.pushButton_group_select_all.clicked.connect(self.__onClearAndResetButtonClicked)
        self.pushButton_group_reset.clicked.connect(self.__onClearAndResetButtonClicked)
        self.pushButton_mask_select_all.clicked.connect(self.__onClearAndResetButtonClicked)
        self.pushButton_mask_reset.clicked.connect(self.__onClearAndResetButtonClicked)

        self.pushButton_clear.clicked.connect(self.__onDeviceControl)
        self.pushButton_load.clicked.connect(self.__onDeviceControl)
        self.pushButton_reset.clicked.connect(self.__onReset)
        self.pushButton_apply.clicked.connect(self.__onApply)

        self.listView_group.clicked.connect(self.__onListClicked)
        self.listView_group.doubleClicked.connect(self.__onListDoubleClicked)

        self.listView_mask.clicked.connect(self.__onListClicked)
        self.listView_mask.doubleClicked.connect(self.__onListDoubleClicked)

        self.listView_preview.clicked.connect(self.__onListClicked)

    def __fillMaskList(self):
        FillupListView(self, self.listView_group, self._module.GetGroups())

    def __onListClicked(self, index):
        if self.sender() == self.listView_group:
            group = index.data()
            masks = self._module.GetMasksForGroup(group)
            if masks is not None:
                FillupListView(self, self.listView_mask, masks)
            else:
                ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_NO_MASK)
                return
            alreadyHas = not self._module.SelectGroup(group)
            if alreadyHas:
                selectedMasks = self._module.GetSelectedMaskForGroup(group)
                FillupListViewWithHighlight(self, self.listView_mask, masks, selectedMasks, LIST_SELECTED_COLOR)
                return
            PaintListViewSelectionBackground(self.listView_group.model(), index, LIST_SELECTED_COLOR)
            selected = self._module.GetSelected()
            if len(selected) > 0:
                FillupListView(self, self.listView_preview, selected)

        elif self.sender() == self.listView_mask:
            PaintListViewSelectionBackground(self.listView_mask.model(), index, LIST_SELECTED_COLOR)
            group = self.listView_group.currentIndex().data()
            mask = index.data()
            self._module.SelectMask(group, mask)
            selected = self._module.GetSelected()
            FillupListView(self, self.listView_preview, selected)
        elif self.sender() == self.listView_preview:
            idx = self._module.GetSelectedGroup(self.listView_preview.currentIndex().data())
            i = self.listView_group.model().index(idx, 0)
            self.listView_group.setCurrentIndex(i)
            self.listView_group.clicked.emit(i)



    def __onListDoubleClicked(self, index):
        PaintListViewSelectionBackground(self.sender().model(), index, LIST_NORMAL_COLOR)
        if self.sender() == self.listView_group:
            group = index.data()
            self._module.DropGroup(group)
            selected = self._module.GetSelected()
            if len(selected) > 0:
                FillupListView(self, self.listView_preview, selected)
            else:
                self.listView_preview.setModel(None)
            self.listView_mask.setModel(None)
        elif self.sender() == self.listView_mask:
            group = self.listView_group.currentIndex().data()
            mask = index.data()
            self._module.DropMask(group, mask)
            selected = self._module.GetSelected()
            FillupListView(self, self.listView_preview, selected)

    def __onSearch(self):
        if self.lineEdit_mask_search.text() == "":
            ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_INVALID_PARAM)
        else:
            idx = self._module.SearchMask(self.listView_group.currentIndex().data(), self.lineEdit_mask_search.text())
            if idx == -1:
                ShowMessageDialog(MESSAGE_TYPE_WARNING, MESSAGE_STR_SEARCH_FAILED)
                return
            else:
                i = self.listView_mask.model().item(idx, 0).index()
                self.listView_mask.setCurrentIndex(i)

    def __onCheckBoxChecked(self, isChecked):
        self._module.UpdateEnableLogMask(self.sender().accessibleName(), isChecked)

    def __onClearAndResetButtonClicked(self):
        if self.sender() == self.pushButton_group_select_all:
            ListViewClickAllItem(self.listView_group)
        elif self.sender() == self.pushButton_group_reset:
            if len(self._module.GetSelected()) == 0:
                return
            ListViewDoubleClickedAllItem(self.listView_group)
            self.listView_group.setCurrentIndex(self.listView_group.model().index(-1, 0))
        elif self.sender() == self.pushButton_mask_select_all:
            ListViewClickAllItem(self.listView_mask)
        elif self.sender() == self.pushButton_mask_reset:
            if len(self._module.GetSelectedMaskForGroup(self.listView_group.currentIndex().data())) == 0:
                return
            ListViewDoubleClickedAllItem(self.listView_mask)
            self.listView_mask.setCurrentIndex(self.listView_mask.model().index(-1, 0))

    def __loadSettingFromFile(self):
        res = self._module.LoadSettingsFromFile()
        if res == ERROR_CODE_SUCCESS:
            self.listView_mask.setModel(None)
            selectedGroup = self._module.GetSelectedGroups()
            FillupListViewWithHighlight(self, self.listView_group, self._module.GetGroups(), selectedGroup,
                                        LIST_SELECTED_COLOR)
            self.listView_group.setCurrentIndex(self.listView_group.model().index(-1, 0))
            enabled = self._module.GetEnableLogMasks()
            for i in range(len(self.__checkBoxs)):
                self.__checkBoxs[i].setChecked(enabled[i][1])
            selected = self._module.GetSelected()
            FillupListView(self, self.listView_preview, selected)
            self.onLogGroupSelectionChanged(True)
        return res

    def __onDeviceControl(self):
        if self.sender() == self.pushButton_clear:
            res = self._module.DropSettingsFromFile()
            if res == ERROR_CODE_ADB_PULL_NOT_EXIST:
                # no need to clear, return success
                res = ERROR_CODE_SUCCESS
            self.__loadSettingFromFile()
            self.__ShowMessage(res)
        elif self.sender() == self.pushButton_load:
            res = self.__loadSettingFromFile()
            self.__ShowMessage(res)

    def __onReset(self):
        self.pushButton_group_reset.clicked.emit()
        enabled = self._module.ResetEnableLogMask()
        for i in range(len(self.__checkBoxs)):
            self.__checkBoxs[i].setChecked(enabled[i][1])


    def __onApply(self):
        res = self._module.ApplySettings()
        self.__ShowMessage(res)

    def __ShowMessage(self, errorCode):
        type, msg = ErrorCodeToMessage(errorCode)
        if errorCode == ERROR_CODE_ADB_PULL_FAILED:
            msg = "%s\n      %s" % (msg, CAMX_OVERRIDE_SETTINGS_PATH)
        elif errorCode == ERROR_CODE_ADB_PUSH_FAILED:
            msg = "%s\n      %s" % (msg, CAMX_OVERRIDE_SETTINGS_ROOT)
        ShowMessageDialog(type, msg)

    def onParseSuccess(self):
        self._module.Update()
        self.listView_mask.setModel(None)
        self.listView_group.setModel(None)
        self.listView_preview.setModel(None)
        self.__fillMaskList()

    def onLogGroupSelectionChanged(self, isEmpty):
        if not isEmpty:
            self.label_current_group.setText("%s %s"% (CURRENT_GROUP_PREFIX, self.listView_group.currentIndex().data()))
        else:
            self.label_current_group.setText(CURRENT_GROUP_PREFIX)
        self.pushButton_mask_search.setEnabled(not isEmpty)
        self.lineEdit_mask_search.setText("")
        self.lineEdit_mask_search.setEnabled(not isEmpty)
        self.pushButton_mask_select_all.setEnabled(not isEmpty)
        self.pushButton_mask_reset.setEnabled(not isEmpty)
