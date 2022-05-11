import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from module.levelModule import LevelModule
from module.pullModule import PullModule
from module.generalSetings import GeneralSettings
from module.autoUpdate import AutoUpdate
if __name__ == "__main__":
    # # module = LevelModule()
    # module = PullModule(GeneralSettings())
    # # path = "C:\\Users\\Alan\\Desktop\\test.txt"
    # path = "C:\\Users\\Alan\\Desktop\\data"
    # # module.DropSettingsFromFile(path)
    # # module.Update()
    # # module.LoadSettingsFromFile(path)
    # module.Merge(path, path)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    update = AutoUpdate()
    update.CheckUpdate()
    sys.exit(app.exec_())

