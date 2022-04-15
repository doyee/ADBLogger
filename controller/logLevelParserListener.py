from abc import abstractmethod


class LogLevelParserListener(object):

    @abstractmethod
    def onParseSuccess(self):
        pass