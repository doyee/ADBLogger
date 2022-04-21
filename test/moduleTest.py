from module.levelModule import LevelModule
from module.pullModule import PullModule
if __name__ == "__main__":
    # module = LevelModule()
    module = PullModule()
    # path = "C:\\Users\\Alan\\Desktop\\test.txt"
    path = "C:\\Users\\Alan\\Desktop\\data"
    # module.DropSettingsFromFile(path)
    # module.Update()
    # module.LoadSettingsFromFile(path)
    module.Merge(path, path)

