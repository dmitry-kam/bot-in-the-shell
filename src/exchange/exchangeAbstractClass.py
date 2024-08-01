from abc import ABC, abstractmethod
class exchangeAbstractClass(ABC):
    session=None

    def connect(self):
        print('Exchange Abstract Class')

    @abstractmethod
    def balance(self):
        pass