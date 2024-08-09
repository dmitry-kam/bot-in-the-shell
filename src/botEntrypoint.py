from elasticsearch import Elasticsearch
from cache import redis
import importlib
import datetime
import psycopg2
import orjson
import time
import os

class BotEntrypointClass():
    # Singleton pattern
    botInstance = None

    # attributes
    exchangeInstance = None
    tradingConfig = None
    cache = None
    cacheSubscriber = None
    elasticSearchConnection = None
    databaseConnection = None
    loggers = []
    signals = []

    def __new__(cls, *args, **kwargs):
        if cls.botInstance is None:
            cls.botInstance = object.__new__(cls, *args, **kwargs)
        return cls.botInstance

    def __init__(self):
        self.initCache()
        self.setLoggers()
        self.initExchange()
        self.loadTradingConfig()

        self.startBot()

    def __del__(self):
        print('Bot has stopped')

    def initCache(self):
        self.cache = redis.RedisCustom()
        print('Init subscribers')
        self.cacheSubscriber = self.cache.redisConnection.pubsub()
        self.cacheSubscriber.psubscribe(**{self.cache.logsChannel: self.handleLogMessage})

    def initElastic(self):
        self.elasticSearchConnection = Elasticsearch(os.environ['ELASTICSEARCH_HOST'])
        print('Init ES')

    def initDatabase(self):
        dbParams = {
            'dbname': os.environ['POSTGRES_DB'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD'],
            'host': os.environ['POSTGRES_HOST'],
            'port': os.environ['POSTGRES_PORT']
        }
        self.databaseConnection = psycopg2.connect(**dbParams)
        self.databaseCursor = self.connection.cursor()
        print('Init DB')

    def initExchange(self):
        exchangeStrategy = importlib.import_module('exchange.' + os.environ['EXCHANGE'] + 'Strategy')
        exchangeClass = getattr(exchangeStrategy, os.environ['EXCHANGE'] + 'Strategy')
        self.exchangeInstance = exchangeClass()
        self.exchangeInstance.connect()
        del exchangeStrategy, exchangeClass
        
        self.exchangeInstance.initCache(self.cache)

    def setLoggers(self):
        loggersList = os.environ['LOGGERS_LIST'].split(',')
        loggersStrategies = importlib.import_module('logger')

        for loggerName in loggersStrategies.__all__:
            loggerClass = importlib.import_module('logger.' + loggerName)
            loggerClass = getattr(loggerClass, loggerName)
            if loggerClass.isSuitable(loggersList):
                self.loggers.append(loggerClass())

        del loggersList, loggersStrategies, loggerName

    def handleLogMessage(self, channelEvent):
        try:
            messageDTO = orjson.loads(channelEvent['data'])
            level, message, context, time = (messageDTO['level'], messageDTO['message'],
                                             messageDTO['context'], messageDTO['time'])
            for logger in self.loggers:
                logger.log(level, message, context, time)
        except Exception as e:
            print('Bad log message! ' + str(e))

    def setSignals(self):
        pass
        #module = importlib.import_module('signalX.' + os.environ['SIGNAL_HANDLER'])
        # signalClass = getattr(module, os.environ['SIGNAL_HANDLER'])
        # signalInstance = signalClass()
        # signalInstance.move()

    def selfCheck(self):
        # todo каждый час
        print('selfCheck')

    def loadTradingConfig(self):
        configPath = os.path.dirname(os.path.realpath(__file__)) + '/../' + os.environ['TRADING_STRATEGY_CONFIG']
        try:
            if os.path.isfile(configPath):
                with open(configPath) as file:
                    self.tradingConfig = orjson.loads(file.read())
                    file.close()

            if self.tradingConfig is None:
                raise Exception("Bad JSON")
            else:
                self.cache.sendMessage('OK', 'Trading strategy has loaded - ' + configPath, self.tradingConfig)
        except Exception as e:
            self.cache.sendMessage('CRITICAL', 'Can\'t load trading config - ' + configPath, {"error": e})
        finally:
            del configPath

    def loadStrategies(self):
        strategyNames = os.getenv('SIGNAL_STRATEGIES', '').split(',')
        strategies = []

        for name in strategy_names:
            module = __import__('signalX', fromlist=[name])
            strategy_class = getattr(module, name)
            strategies.append(strategy_class())

        return strategies

    def startBot(self):
        self.cache.sendMessage('OK', 'Bot has been launched', {})

        # todo: условия что все ок
        while True:
            self.cacheSubscriber.get_message()

            time.sleep(3)
            #time.sleep(int(os.environ['SLEEP_DURATION']))


x = BotEntrypointClass()

# self.cache.set('timeY', time.time())
# self.exchangeInstance.getBalance()