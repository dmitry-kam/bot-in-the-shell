from abc import ABC, abstractmethod
import redis
import os

class exchangeAbstractClass(ABC):
    session=None
    cache=None

    def connect(self):
        print('Exchange Abstract Class')

    def initCache(self):
        self.cache = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

    @abstractmethod
    def getBalance(self):
        pass