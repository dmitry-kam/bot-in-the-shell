from .signalClass import SignalClass


class signalOne(SignalClass):



    @staticmethod
    def isSuitable(names: list) -> bool:
        return __class__.__name__ in names

    def setStrategyName(self):
        self.strategyName = __class__.__name__

    def calculate(self, ticker: str, current_price: float) -> dict:
        probabilities = {
            "buy": 0.5,
            "sell": 0.3,
            "hold": 0.2,
            "modifiers": [],
            "blockers": []
        }
        return probabilities