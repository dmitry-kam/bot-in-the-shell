import os
import signalX as signalX
import importlib

class BotEntrypointClass():
    # Singleton pattern
    obj = None
    # attributes
    exchange = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj
    def __init__(self):
        print('BotConstructor')
        self.startBot(self)
        #print(signalX.__dict__)
        module = importlib.import_module('signalX.' + os.environ['SIGNAL_HANDLER'])
        signalClass = getattr(module, os.environ['SIGNAL_HANDLER'])
        signalInstance = signalClass()
        signalInstance.move()

        ###############3

        exchangeStrategy = importlib.import_module('exchange.' + os.environ['EXCHANGE'] + 'Strategy')
        print('++++++++++++++++++++++++++++')
        exchangeClass = getattr(exchangeStrategy, os.environ['EXCHANGE'] + 'Strategy')
        exchangeInstance = exchangeClass()
        exchangeInstance.connect()
        exchangeInstance.balance()

        pass

    @staticmethod
    def startBot(self):
        print('Start bot')


x = BotEntrypointClass()
