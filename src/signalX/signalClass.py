from abc import ABC, abstractmethod
class SignalClass(ABC):

    def func(self):
        print('SignalClass')

    @abstractmethod
    def move(self):
        pass