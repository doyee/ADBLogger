from module.adbManager import ADBManager

if __name__ == "__main__":
    manager = ADBManager.get_instance()
    manager.CheckADB()
    manager.GetDeviceInfo()