from abc import abstractmethod


class AutoUpdateListener(object):
    @abstractmethod
    def onCheckUpdate(self, hasNewVersion, lastestVersion):
        pass