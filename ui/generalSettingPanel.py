from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QLabel, QSizePolicy, QSpacerItem

from ui.settingDialog import SettingDialog

class GeneralSettingPanel(SettingDialog):

    def __init__(self, parent, size, module):
        super().__init__(parent, size)
        self.__module = module

    def setupUi(self):
        self.verticalLayout_dir = QVBoxLayout()
        self.verticalLayout_dir.setObjectName(u"verticalLayout_dir")
        self.__checkBox_dir = QCheckBox(self)
        self.__checkBox_dir.setObjectName(u"__checkBox_dir")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.__checkBox_dir.sizePolicy().hasHeightForWidth())
        self.__checkBox_dir.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.__checkBox_dir.setFont(font)

        self.verticalLayout_dir.addWidget(self.__checkBox_dir)

        self._verticalLayout_main.addLayout(self.verticalLayout_dir)

        self.__verticalLayout_file = QVBoxLayout()
        self.__verticalLayout_file.setObjectName(u"__verticalLayout_file")
        self.__checkBox_file = QCheckBox(self)
        self.__checkBox_file.setObjectName(u"__checkBox_file")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.__checkBox_file.sizePolicy().hasHeightForWidth())
        self.__checkBox_file.setSizePolicy(sizePolicy1)
        self.__checkBox_file.setFont(font)

        self.__verticalLayout_file.addWidget(self.__checkBox_file)

        self.__label_file_info = QLabel(self)
        self.__label_file_info.setObjectName(u"__label_file_info")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.__label_file_info.sizePolicy().hasHeightForWidth())
        self.__label_file_info.setSizePolicy(sizePolicy2)

        self.__verticalLayout_file.addWidget(self.__label_file_info)

        self.__label_file_exe = QLabel(self)
        self.__label_file_exe.setObjectName(u"__label_file_exe")
        sizePolicy2.setHeightForWidth(self.__label_file_exe.sizePolicy().hasHeightForWidth())
        self.__label_file_exe.setSizePolicy(sizePolicy2)

        self.__verticalLayout_file.addWidget(self.__label_file_exe)

        self._verticalLayout_main.addLayout(self.__verticalLayout_file)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self._verticalLayout_main.addItem(self.verticalSpacer)

        super().setupUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("SettingDialog", u"通用设置", None))
        self.__checkBox_dir.setText(QCoreApplication.translate("SettingDialog", u"\u5408\u5e76log\u540e\u6253\u5f00log\u6240\u5728\u76ee\u5f55", None))
        self.__checkBox_file.setText(QCoreApplication.translate("SettingDialog", u"\u5408\u5e76\u540e\u6253\u5f00log\u6587\u4ef6", None))
        self.__label_file_info.setText(QCoreApplication.translate("SettingDialog",u"\u76ee\u524d\u53ea\u652f\u6301\u4f7f\u7528notepadd++\u6216TextAnalysisTool.NET\u6253\u5f00",None))
        self.__label_file_exe.setText(QCoreApplication.translate("SettingDialog",u"",None))
        self._pushButton_apply.setText(QCoreApplication.translate("SetingDialog", u"应用", None))
        super().retranslateUi()

    def _cancel(self):
        self._reset()
        self.close()