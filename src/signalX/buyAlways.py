from .signalClass import SignalClass


class buyAlways(SignalClass):

    @staticmethod
    def isSuitable(names: list) -> bool:
        return __class__.__name__ in names

    def setSignalName(self):
        self.signalName = __class__.__name__

    def getWeightedForecast(self, time: str) -> dict:
        self.signalAnswer['BUY'] = 1.0 * self.signalWeight
        return self.signalAnswer