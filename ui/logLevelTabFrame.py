from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.tabFrame import TabFrame


class LogLevelTabFrame(TabFrame):

    def __init__(self, module, parent=None):
        super().__init__(module, parent)
        self.setupUi(self)


    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        self.verticalLayoutWidget = QWidget(Frame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 640, 480))
        self.verticalLayout_main = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_settings = QHBoxLayout()
        self.horizontalLayout_settings.setObjectName(u"horizontalLayout_settings")
        self.verticalLayout_group = QVBoxLayout()
        self.verticalLayout_group.setObjectName(u"verticalLayout_group")
        self.horizontalLayout_group_heading = QHBoxLayout()
        self.horizontalLayout_group_heading.setObjectName(u"horizontalLayout_group_heading")
        self.label_group = QLabel(self.verticalLayoutWidget)
        self.label_group.setObjectName(u"label_group")

        self.horizontalLayout_group_heading.addWidget(self.label_group)

        self.pushButton_group_reset = QPushButton(self.verticalLayoutWidget)
        self.pushButton_group_reset.setObjectName(u"pushButton_group_reset")

        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_reset)

        self.pushButton_group_select_all = QPushButton(self.verticalLayoutWidget)
        self.pushButton_group_select_all.setObjectName(u"pushButton_group_select_all")

        self.horizontalLayout_group_heading.addWidget(self.pushButton_group_select_all)


        self.verticalLayout_group.addLayout(self.horizontalLayout_group_heading)

        self.listView_group = QListView(self.verticalLayoutWidget)
        self.listView_group.setObjectName(u"listView_group")

        self.verticalLayout_group.addWidget(self.listView_group)


        self.horizontalLayout_settings.addLayout(self.verticalLayout_group)

        self.verticalLayout_mask = QVBoxLayout()
        self.verticalLayout_mask.setObjectName(u"verticalLayout_mask")
        self.horizontalLayout_mask_heading = QHBoxLayout()
        self.horizontalLayout_mask_heading.setObjectName(u"horizontalLayout_mask_heading")
        self.label_mask = QLabel(self.verticalLayoutWidget)
        self.label_mask.setObjectName(u"label_mask")

        self.horizontalLayout_mask_heading.addWidget(self.label_mask)

        self.pushButton_mask_reset = QPushButton(self.verticalLayoutWidget)
        self.pushButton_mask_reset.setObjectName(u"pushButton_mask_reset")

        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_reset)

        self.pushButton_mask_select_all = QPushButton(self.verticalLayoutWidget)
        self.pushButton_mask_select_all.setObjectName(u"pushButton_mask_select_all")

        self.horizontalLayout_mask_heading.addWidget(self.pushButton_mask_select_all)


        self.verticalLayout_mask.addLayout(self.horizontalLayout_mask_heading)

        self.listView_mask = QListView(self.verticalLayoutWidget)
        self.listView_mask.setObjectName(u"listView_mask")

        self.verticalLayout_mask.addWidget(self.listView_mask)


        self.horizontalLayout_settings.addLayout(self.verticalLayout_mask)


        self.verticalLayout_main.addLayout(self.horizontalLayout_settings)

        self.label_preview = QLabel(self.verticalLayoutWidget)
        self.label_preview.setObjectName(u"label_preview")

        self.verticalLayout_main.addWidget(self.label_preview)

        self.listView_preview = QListView(self.verticalLayoutWidget)
        self.listView_preview.setObjectName(u"listView_preview")

        self.verticalLayout_main.addWidget(self.listView_preview)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.pushButton_6 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_buttons.addWidget(self.pushButton_6)

        self.pushButton_clear = QPushButton(self.verticalLayoutWidget)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.horizontalLayout_buttons.addWidget(self.pushButton_clear)

        self.horizontalSpacer_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer_buttons)

        self.pushButton_apply = QPushButton(self.verticalLayoutWidget)
        self.pushButton_apply.setObjectName(u"pushButton_apply")

        self.horizontalLayout_buttons.addWidget(self.pushButton_apply)


        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_group.setText(QCoreApplication.translate("Form", u"Group", None))
        self.pushButton_group_reset.setText(QCoreApplication.translate("Form", u"\u91cd\u7f6e", None))
        self.pushButton_group_select_all.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.label_mask.setText(QCoreApplication.translate("Form", u"Mask", None))
        self.pushButton_mask_reset.setText(QCoreApplication.translate("Form", u"\u91cd\u7f6e", None))
        self.pushButton_mask_select_all.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.label_preview.setText(QCoreApplication.translate("Form", u"\u9884\u89c8", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"\u8bfb\u53d6\u8bbe\u5907\u9884\u8bbe", None))
        self.pushButton_clear.setText(QCoreApplication.translate("Form", u"\u6e05\u9664\u8bbe\u5907\u9884\u8bbe", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Form", u"\u5e94\u7528", None))
    # retranslateUi

