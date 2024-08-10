from abc import ABC, abstractmethod


class SignalClass(ABC):
    # any strategy should have all tools
    tradingConfig = None
    signalConfig = None
    cache = None
    elasticSearchConnection = None
    databaseConnection = None

    strategyName = None
    strategyAnswer = {
        "BUY": None,
        "SELL": None,
        "HOLD": None,
        "WAIT": None,
        "MODIFIERS": [],
        "BLOCKERS": []
    }

    @staticmethod
    def isSuitable(names: list) -> bool:
        return __class__.__name__ in names

    def __init__(self, tradingConfig, cache, elasticSearchConnection, databaseConnection):
        self.tradingConfig = tradingConfig
        self.setStrategyName()
        self.signalConfig = tradingConfig['SIGNALS'][self.strategyName]
        self.cache = cache
        self.elasticSearchConnection = elasticSearchConnection
        self.databaseConnection = databaseConnection
        self.sendMessage('INFO', 'Init Signal - ' + self.strategyName, self.signalConfig)

    def sendMessage(self, level: str, message: str, context: dict):
        self.cache.sendMessage(level, message, context)

    @abstractmethod
    def setStrategyName(self):
        pass

    @abstractmethod
    def calculate(self, ticker: str, currentPrice: float) -> dict:
        pass