from .exchangeAbstractClass import exchangeAbstractClass
from elasticsearch import Elasticsearch
from datetime import datetime
import os


class TestStrategy(exchangeAbstractClass):
    marketSequence = None
    marketSequenceGenerator = None

    def connect(self):
        self.sendMessage('INFO', 'TestStrategy has chosen', {})
        self.session = Elasticsearch(os.environ['ELASTICSEARCH_HOST'])

        # sorted history of market
        index = "daily_" + self.config['COIN'].lower()
        self.marketSequence = self.session.search(index=index, query={"match_all": {}}, size=10000, sort='timeOpen')
        self.marketSequence = self.marketSequence['hits']['hits'][7:]

        self.sendMessage(
                    'DEBUG',
                         'Market sequence from ' +
                         self.marketSequence[self.config['START_SEQUENCE_DAY']]['_id'] +
                         ' to ' + self.marketSequence[self.config['END_SEQUENCE_DAY']]['_id'],
                    {
                        'START_PRICE': self.marketSequence[self.config['START_SEQUENCE_DAY']]['_source']['avgPrice'],
                        'END_PRICE': self.marketSequence[self.config['END_SEQUENCE_DAY']]['_source']['avgPrice']
                    })

        self.marketSequence = self.marketSequence[self.config['START_SEQUENCE_DAY']:self.config['END_SEQUENCE_DAY']]
        self.marketSequenceGenerator = self.getPriceGenerator()

    def getBalance(self):
        self.cache.setKeyValue('BALANCE_' + self.config['STABLECOIN'], self.config['STABLECOIN_DEPOSIT'])
        self.cache.setKeyValue('BALANCE_' + self.config['COIN'], 0)
        pass

    def placeOrder(self):
        pass

    def getMarketData(self, symbol):
        try:
            return next(self.marketSequenceGenerator)
        except StopIteration:
            return None

    # ordered by time price generator
    def getPriceGenerator(self):
        for currentDay in self.marketSequence:
            currentDay = currentDay['_source']

            timeHigh = datetime.fromisoformat(currentDay['timeHigh'])
            timeLow = datetime.fromisoformat(currentDay['timeLow'])
            timeAvg = str((max(timeHigh, timeLow) - min(timeHigh, timeLow)) / 2 + min(timeHigh, timeLow))

            currentDayPrices = {
                currentDay['timeOpen']: currentDay['openPrice'],
                currentDay['timeHigh']: currentDay['highPrice'],
                timeAvg: currentDay['avgPrice'],
                currentDay['timeLow']: currentDay['lowPrice'],
                currentDay['timeClose']: currentDay['closePrice'],
            }

            currentDayPrices = dict(sorted(currentDayPrices.items(), key = lambda x:x[0]))

            for time, price in currentDayPrices.items():
                yield {'price': price, 'time': time}
                next(iter(currentDayPrices))

    def cancelOder(self, orderId):
        pass

    def checkOrder(self, orderId):
        pass

    def checkCandle(self, currentDeposit: float) -> bool:
        # always enough
        return True
