from .exchangeAbstractClass import exchangeAbstractClass
import binance
import os
class BinanceStrategy(exchangeAbstractClass):
    def connect(self):
        print('BinanceStrategy')
        print('=============')

    def balance(self):
        print('can\'t do it')
