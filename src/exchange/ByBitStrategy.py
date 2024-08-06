from .exchangeAbstractClass import exchangeAbstractClass
from pybit.unified_trading import HTTP
import os

class ByBitStrategy(exchangeAbstractClass):
    def connect(self):
        print('ByBitStrategy has chosen')
        self.session = HTTP(
            testnet=False,
            api_key=os.environ['API_KEY'],
            api_secret=os.environ['SECRET_KEY'],
        )

    def getBalance(self):
        # print(session.get_orderbook(category="linear", symbol="BTCUSDT"))
        balanceAnswer = self.session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT,ETH"
        )
        #print(balanceAnswer)

        for coinBalance in balanceAnswer['result']['list'][0]['coin']:
            print(coinBalance['walletBalance'])
            print(coinBalance['coin'])
            self.cache.set(coinBalance['coin'], coinBalance['walletBalance'])

    def placeOrder(self):
        print(self.session.place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty=0.001,
        ))
