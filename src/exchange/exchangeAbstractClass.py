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


    # todo принимать числа