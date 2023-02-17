import os
# from signal.signal import SignalClass
# from src.signal.signal import SignalChange
import src.signalX as signalX
import importlib


class BotEntrypointClass():#SignalChange
    def __init__(self):
        print('Constructor')
        self.startBot(self)
        #print(signalX.__dict__)
        module = importlib.import_module('src.signalX.' + os.environ['SIGNAL_HANDLER'])
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


def ssss():
    print('Start')
