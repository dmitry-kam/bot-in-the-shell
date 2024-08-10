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
        self.initElastic()
        self.initDatabase()
        self.initExchange()
        self.loadTradingConfig()
        self.setSignals()

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
        self.sendMessage('INFO', 'Init ES', {})

    def initDatabase(self):
        dbParams = {
            'dbname': os.environ['POSTGRES_DB'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD'],
            'host': os.environ['POSTGRES_HOST'],
            'port': os.environ['POSTGRES_PORT']
        }
        self.databaseConnection = psycopg2.connect(**dbParams)
        self.databaseCursor = self.databaseConnection.cursor()
        self.sendMessage('INFO', 'Init DB', {})
        del dbParams

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
        loggerName = None

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
            self.sendMessage('WARNING', 'Bad log message! ' + str(e), {})

    def setSignals(self):
        signalList = list(self.tradingConfig['SIGNALS'].keys())
        signalStrategies = importlib.import_module('signalX')
        signalName = None

        for signalName in signalStrategies.__all__:
            signalClass = importlib.import_module('signalX.' + signalName)
            signalClass = getattr(signalClass, signalName)
            if signalClass.isSuitable(signalList):
                self.signals.append(signalClass(
                    self.tradingConfig,
                    self.cache,
                    self.elasticSearchConnection,
                    self.databaseConnection
                ))

        del signalList, signalStrategies, signalName

    def selfCheck(self):
        # todo каждый час
        print('selfCheck')

    def sendMessage(self, level: str, message: str, context: dict):
        self.cache.sendMessage(level, message, context)

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
                self.sendMessage('OK', 'Trading strategy has loaded - ' + configPath, self.tradingConfig)
        except Exception as e:
            self.sendMessage('CRITICAL', 'Can\'t load trading config - ' + configPath, {"error": e})
        finally:
            del configPath

    def startBot(self):
        self.sendMessage('OK', 'Bot has been launched', {})

        # todo: условия что все ок
        while True:
            self.cacheSubscriber.get_message()

            time.sleep(3)
            #time.sleep(int(os.environ['SLEEP_DURATION']))


x = BotEntrypointClass()

# self.cache.set('timeY', time.time())
# self.exchangeInstance.getBalance()