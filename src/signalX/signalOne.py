from .signalClass import SignalClass


class signalOne(SignalClass):

    @staticmethod
    def isSuitable(names: list) -> bool:
        return __class__.__name__ in names

    def setSignalName(self):
        self.signalName = __class__.__name__

    def getWeightedForecast(self, time: str) -> dict:
        return self.signalAnswer