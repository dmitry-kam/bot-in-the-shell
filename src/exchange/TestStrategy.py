from .exchangeAbstractClass import exchangeAbstractClass
import os


class TestStrategy(exchangeAbstractClass):
    def connect(self):
        pass

    def getBalance(self):
        pass

    def placeOrder(self):
        pass
