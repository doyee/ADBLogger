from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller.logLevelParserListener import LogLevelParserListener
from module.levelModule import LogMaskSelectionListener
from ui.tabFrame import TabFrame
from utils.Utils import *
from utils.UIUtils import *

CURRENT_GROUP_PREFIX = u"当前选择的Group:"

class LogLevelTabFrame(TabFrame, LogLevelParserListener, LogMaskSelectionListener):

    def __init__(self, module, parent=None):
        super().__init__(module, parent)

    def layout(self):
        self.verticalLayout_main = QVBoxLayout(self)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_settings = QHBoxLayout()
        self.horizontalLayout_settings.setObjectName(u"horizontalLayout_settings")
        self.verticalLayout_group = QVBoxLayout()
        self.verticalLayout_group.setObjectName(u"verticalLayout_group")
        self.horizontalLayout_group_heading = QHBoxLayout()
        self.horizontalLayout_group_heading.setObjectName(u"horizontalLayout_group_heading")
        self.label_group = QLabel(self)
        self.label_group.setObjectName(u"label_group")

        self.horizontalLayout_group_heading.addWidget(self.label_group)

        self.pushButton_group_reset = QPushButton(self)
        self.pushButton_group_reset.setObjectName(u"pushButton_group_reset")

        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_reset)

        self.pushButton_group_select_all = QPushButton(self)
        self.pushButton_group_select_all.setObjectName(u"pushButton_group_select_all")

        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_select_all)

        self.verticalLayout_group.addLayout(self.horizontalLayout_group_heading)

        self.label_current_group = QLabel(self)
        self.label_current_group.setObjectName(u"label_current_group")
        self.label_current_group.setContentsMargins(0, 5, 0, 5)

        self.verticalLayout_group.addWidget(self.label_current_group)

        self.listView_group = QListView(self)
        self.listView_group.setObjectName(u"listView_group")
        self.__fillMaskList()
        self.verticalLayout_group.addWidget(self.listView_group)

        self.horizontalLayout_settings.addLayout(self.verticalLayout_group)

        self.verticalLayout_mask = QVBoxLayout()
        self.verticalLayout_mask.setObjectName(u"verticalLayout_mask")
        self.horizontalLayout_mask_heading = QHBoxLayout()
        self.horizontalLayout_mask_heading.setObjectName(u"horizontalLayout_mask_heading")
        self.label_mask = QLabel(self)
        self.label_mask.setObjectName(u"label_mask")

        self.horizontalLayout_mask_heading.addWidget(self.label_mask)

        self.pushButton_mask_reset = QPushButton(self)
        self.pushButton_mask_reset.setObjectName(u"pushButton_mask_reset")

        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_reset)

        self.pushButton_mask_select_all = QPushButton(self)
        self.pushButton_mask_select_all.setObjectName(u"pushButton_mask_select_all")

        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_select_all)

        self.verticalLayout_mask.addLayout(self.horizontalLayout_mask_heading)

        self.horizontalLayout_search = QHBoxLayout()
        self.horizontalLayout_search.setObjectName(u"horizontalLayout_search")
        self.lineEdit_mask_search = QLineEdit(self)
        self.lineEdit_mask_search.setEnabled(False)
        self.lineEdit_mask_search.setObjectName(u"lineEdit_mask_search")
        self.lineEdit_mask_search.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_search.addWidget(self.lineEdit_mask_search)

        self.pushButton_mask_search = QPushButton(self)
        self.pushButton_mask_search.setEnabled(False)
        self.pushButton_mask_search.setObjectName(u"pushButton_mask_search")

        self.horizontalLayout_search.addWidget(self.pushButton_mask_search)

        self.verticalLayout_mask.addLayout(self.horizontalLayout_search)

        self.listView_mask = QListView(self)
        self.listView_mask.setObjectName(u"listView_mask")

        self.verticalLayout_mask.addWidget(self.listView_mask)

        self.horizontalLayout_settings.addLayout(self.verticalLayout_mask)

        self.verticalLayout_main.addLayout(self.horizontalLayout_settings)

        self.horizontalLayout_check = QHBoxLayout()
        self.horizontalLayout_check.setObjectName(u"horizontalLayout_check")

        enableLogMask = self._module.GetEnableLogMasks()
        for i in range(len(enableLogMask)):
            checkbox = QCheckBox(self)
            des = enableLogMask[i][0]
            checkbox.setObjectName("checkbox_%s" % des)
            checkbox.setAccessibleName(des)
            checkbox.setText(des)
            checkbox.setChecked(enableLogMask[i][1])
            checkbox.clicked.connect(self.__onCheckBoxChecked)
            self.horizontalLayout_check.addWidget(checkbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_check.addItem(self.horizontalSpacer)

        self.verticalLayout_main.addLayout(self.horizontalLayout_check)

        self.label_preview = QLabel(self)
        self.label_preview.setObjectName(u"label_preview")

        self.verticalLayout_main.addWidget(self.label_preview)

        self.listView_preview = QListView(self)
        self.listView_preview.setObjectName(u"listView_preview")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_preview.sizePolicy().hasHeightForWidth())
        self.listView_preview.setSizePolicy(sizePolicy)
        self.listView_preview.setMaximumSize(QSize(self.geometry().width(), self.geometry().height() / 5))

        self.verticalLayout_main.addWidget(self.listView_preview)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.pushButton_reset = QPushButton(self)
        self.pushButton_reset.setObjectName(u"pushButton_reset")

        self.horizontalLayout_buttons.addWidget(self.pushButton_reset)

        self.pushButton_clear = QPushButton(self)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.horizontalLayout_buttons.addWidget(self.pushButton_clear)

        self.horizontalSpacer_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer_buttons)

        self.pushButton_apply = QPushButton(self)
        self.pushButton_apply.setObjectName(u"pushButton_apply")

        self.horizontalLayout_buttons.addWidget(self.pushButton_apply)

        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)

        self._module.SetListener(self)
        self._module.Update()
        super().layout()

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def _retranslateUi(self):
        self.label_group.setText(QCoreApplication.translate("TabFrame", u"Group", None))
        self.label_current_group.setText(QCoreApplication.translate("TabFrame", CURRENT_GROUP_PREFIX, None))
        self.pushButton_group_reset.setText(QCoreApplication.translate("TabFrame", u"\u91cd\u7f6e", None))
        self.pushButton_group_select_all.setText(QCoreApplication.translate("TabFrame", u"\u5168\u9009", None))
        self.label_mask.setText(QCoreApplication.translate("TabFrame", u"Mask", None))
        self.pushButton_mask_reset.setText(QCoreApplication.translate("TabFrame", u"\u91cd\u7f6e", None))
        self.pushButton_mask_select_all.setText(QCoreApplication.translate("TabFrame", u"\u5168\u9009", None))
        self.lineEdit_mask_search.setPlaceholderText(
            QCoreApplication.translate("TabFrame", u"\u8bf7\u8f93\u5165\u5b8c\u6574mask", None))
        self.pushButton_mask_search.setText(QCoreApplication.translate("TabFrame", u"\u641c\u7d22", None))
        self.pushButton_reset.setText(
            QCoreApplication.translate("TabFrame", u"\u8bfb\u53d6\u8bbe\u5907\u9884\u8bbe", None))
        self.pushButton_clear.setText(
            QCoreApplication.translate("TabFrame", u"\u6e05\u9664\u8bbe\u5907\u9884\u8bbe", None))
        self.pushButton_apply.setText(QCoreApplication.translate("TabFrame", u"\u5e94\u7528", None))

    # retranslateUi

    def _connectUi(self):
        self.pushButton_mask_search.clicked.connect(self.__onSearch)
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
                ShowMessageDialog(MESSAGE_TYPE_NO_MASK)
                return
            alreadyHas = not self._module.SelectGroup(group)
            if alreadyHas:
                selectedMasks = self._module.GetSelectedMaskForGroup(group)
                FillupListViewWithHighlight(self, self.listView_mask, masks, selectedMasks, LIST_SELECTED_COLOR)
                return
            PaintListViewSelectionBackground(self.sender(), LIST_SELECTED_COLOR)
            selected = self._module.GetSelected()
            if len(selected) > 0:
                FillupListView(self, self.listView_preview, selected)

        elif self.sender() == self.listView_mask:
            PaintListViewSelectionBackground(self.sender(), LIST_SELECTED_COLOR)
            group = self.listView_group.currentIndex().data()
            mask = index.data()
            self._module.SelectMask(group, mask)
            selected = self._module.GetSelected()
            FillupListView(self, self.listView_preview, selected)
        elif self.sender() == self.listView_preview:
            idx = self._module.GetSelectedGroup(self.listView_preview.currentIndex().data())
            i = self.listView_group.model().index(idx, 0)
            self.listView_group.clicked.emit(i)
            self.listView_group.setCurrentIndex(i)


    def __onListDoubleClicked(self, index):
        PaintListViewSelectionBackground(self.sender(), LIST_NORMAL_COLOR)
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
            ShowMessageDialog(MESSAGE_TYPE_INVALID_PARAM)
        else:
            idx = self._module.SearchMask(self.listView_group.currentIndex().data(), self.lineEdit_mask_search.text())
            if idx == -1:
                ShowMessageDialog(MESSAGE_TYPE_SEARCH_FAILED)
                return
            else:
                i = self.listView_mask.model().item(idx, 0).index()
                print(i)
                self.listView_mask.setCurrentIndex(i)

    def __onCheckBoxChecked(self, isChecked):
        self._module.UpdateEnableLogMask(self.sender().accessibleName(), isChecked)

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