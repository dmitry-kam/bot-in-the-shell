from abc import ABC, abstractmethod
class SignalClass(ABC):

    def func(self):
        print('SignalClass')

    @abstractmethod
    def move(self):
        pass

class SignalOne(SignalClass):
    def move(self):
        print(111)

class SignalTwo(SignalClass):
    def move(self):
        print(222)
