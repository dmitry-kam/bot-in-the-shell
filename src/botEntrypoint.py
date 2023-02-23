import os
# from signal.signal import SignalClass
# from src.signal.signal import SignalChange
import signalX as signalX
import importlib


class BotEntrypointClass():
    # Singleton pattern
    obj = None
    someattr = 0
    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj
    def __init__(self):
        print('Constructor')
        self.startBot(self)
        #print(signalX.__dict__)
        module = importlib.import_module('signalX.' + os.environ['SIGNAL_HANDLER'])
        print('Change class...')
        print(os.environ['SIGNAL_HANDLER'], type(os.environ['SIGNAL_HANDLER']))
        class_ = getattr(module, os.environ['SIGNAL_HANDLER'])
        instance = class_()
        instance.move()
        pass

    def startBot1():
        print('Start bot')
    @staticmethod
    def startBot(self):
        print('Start bot')

    def ssss(self):
        print('Start', self.someattr)


x = BotEntrypointClass()
x.ssss()
x.someattr = 88
x.ssss()
y = BotEntrypointClass()
y.ssss()