import os
# from signal.signal import SignalClass
# from src.signal.signal import SignalChange
import src.signal.signal as ss
import importlib


class BotEntrypointClass():#SignalChange
    def __init__(self):
        print('Constructor')
        self.startBot(self)
        module = importlib.import_module('src.signal.signal')
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