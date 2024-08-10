from abc import ABC, abstractmethod
import os

class exchangeAbstractClass(ABC):
    session=None
    cache=None

    def connect(self):
        print('Exchange Abstract Class')

    def initCache(self, cacheConnection):
        self.cache = cacheConnection

    @abstractmethod
    def getBalance(self):
        pass


    #
    # @abstractmethod
    # def get_account_balance(self):
    #     pass
    #
    # @abstractmethod
    # def getMarketData(self, symbol):
    #     pass
    #
    # @abstractmethod
    # def placeOrder(self, symbol, quantity, order_type, price=None):
    #     pass
    #
    # @abstractmethod
    # def cancelOder(self, order_id):
    #     pass
    #
    # @abstractmethod
    # def checkOrder(self, order_id):
    #     pass



    # todo принимать числа