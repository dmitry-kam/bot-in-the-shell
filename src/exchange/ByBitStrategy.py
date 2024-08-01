from .exchangeAbstractClass import exchangeAbstractClass
from pybit.unified_trading import HTTP
import os
class ByBitStrategy(exchangeAbstractClass):
    def connect(self):
        print('ByBitStrategy')
        print('=============')
        self.session = HTTP(
            testnet=False,
            api_key=os.environ['API_KEY'],
            api_secret=os.environ['SECRET_KEY'],
        )

    def balance(self):
        # print(session.get_orderbook(category="linear", symbol="BTCUSDT"))
        print(self.session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT"
        ))

        # print(self.session.place_order(
        #     category="linear",
        #     symbol="BTCUSDT",
        #     side="Buy",
        #     orderType="Market",
        #     qty=0.001,
        # ))
