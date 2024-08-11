from elasticsearch import Elasticsearch
from collections import defaultdict
from cache import redis
import importlib
import jstyleson
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
    signalsConfig = None
    cache = None
    cacheSubscriber = None
    elasticSearchConnection = None
    databaseConnection = None
    loggers = []
    signals = []

    # trading
    availableModes = ['BUY', 'SELL', 'HOLD', 'WAIT']
    mode = 'BUY'
    exchangeConfig = None

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
        self.loadSignalsConfig()
        self.setSignals()
        ###############
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
        configPath = os.path.dirname(os.path.realpath(__file__)) + '/../' + os.environ['EXCHANGE_COMMON_PARAMETERS']
        try:
            if os.path.isfile(configPath):
                with open(configPath) as file:
                    self.exchangeConfig = jstyleson.loads(file.read())
                    file.close()

            if self.exchangeConfig is None:
                raise Exception("Bad JSON")
            else:
                exchangeStrategy = importlib.import_module('exchange.' + os.environ['EXCHANGE'] + 'Strategy')
                exchangeClass = getattr(exchangeStrategy, os.environ['EXCHANGE'] + 'Strategy')
                self.exchangeInstance = exchangeClass()
                self.exchangeInstance.initCache(self.cache)
                self.exchangeInstance.initConfig(self.exchangeConfig)
                self.sendMessage('OK', 'Exchange config has loaded - ' + configPath, self.exchangeConfig)
                self.exchangeInstance.connect()
                del exchangeStrategy, exchangeClass
        except Exception as e:
            self.sendMessage('CRITICAL', 'Can\'t load exchange config - ' + configPath, {"error": e})
        finally:
            del configPath

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

    def getAllMessages(self):
        while True:
            message = self.cacheSubscriber.get_message()
            if message and message['type'] == 'message':
                continue
            else:
                break

    def handleLogMessage(self, channelEvent):
        try:
            messageDTO = orjson.loads(channelEvent['data'])
            level, message, context, time = (messageDTO['level'], messageDTO['message'],
                                             messageDTO['context'], messageDTO['time'])
            for logger in self.loggers:
                logger.log(level, message, context, time)
            # recursive check current messages
            self.getAllMessages()
        except Exception as e:
            self.sendMessage('WARNING', 'Bad log message! ' + str(e), {})

    def setSignals(self):
        signalList = list(self.signalsConfig['SIGNALS'].keys())
        signalStrategies = importlib.import_module('signalX')
        signalName = None

        for signalName in signalStrategies.__all__:
            signalClass = importlib.import_module('signalX.' + signalName)
            signalClass = getattr(signalClass, signalName)
            if signalClass.isSuitable(signalList):
                self.signals.append(signalClass(
                    self.signalsConfig,
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

    def loadSignalsConfig(self):
        configPath = os.path.dirname(os.path.realpath(__file__)) + '/../' + os.environ['TRADING_STRATEGY_CONFIG']
        try:
            if os.path.isfile(configPath):
                with open(configPath) as file:
                    self.signalsConfig = jstyleson.loads(file.read())
                    file.close()

            if self.signalsConfig is None:
                raise Exception("Bad JSON")
            else:
                self.sendMessage('OK', 'Trading strategy has loaded - ' + configPath, self.signalsConfig)
        except Exception as e:
            self.sendMessage('CRITICAL', 'Can\'t load trading config - ' + configPath, {"error": e})
        finally:
            del configPath

    def setMode(self, mode):
        if mode in self.availableModes:
            self.mode = mode
            self.cache.setKeyValue('BOT_MODE', mode)
        else:
            self.sendMessage('ERROR', 'Unknown mode: ' + mode, {'currentMode': self.mode})

    def getMode(self):
        return self.mode

    def aggregateAnswer(self, decisions):
        sums = defaultdict(float)
        counts = defaultdict(int)
        uniqueModifiers = set()
        uniqueBlockers = set()

        for entry in decisions:
            for key in self.availableModes:
                value = entry.get(key)
                if value is not None:
                    sums[key] += value
                    counts[key] += 1

            uniqueModifiers.update(entry.get('MODIFIERS', []))
            uniqueBlockers.update(entry.get('BLOCKERS', []))

        answer = {key: (sums[key] / counts[key]) if counts[key] > 0 else None for key in self.availableModes}

        answer['MODIFIERS'] = list(uniqueModifiers)
        answer['BLOCKERS'] = list(uniqueBlockers)

        return answer

    def makeDecision(self, forecast):
        print("##### Сегодня " + source['timeOpen'] + ". У меня " + str(deposit) + "$$$")
        if waitMode == False:
            if currentOrderType == "BUY":
                makeOrder((source['openPrice'] if closedAll == 0 else source['closePrice']) * 0.97)
            elif currentOrderType == "SELL":
                makeOrder(source['openPrice'] * 1.03)

            print("===== Жду закрытия ордера " + currentOrderType + " уже " + str(wait) + "дней")
            if checkOrder(source):
                currentOrderType = "BUY" if currentOrderType == "SELL" else "SELL"
        else:
            print("===== Жду закрытия ордера " + currentOrderType + " уже " + str(wait) + "дней")
            if checkOrder(source):
                currentOrderType = "BUY" if currentOrderType == "SELL" else "SELL"


    def startBot(self):
        self.sendMessage('OK', 'Bot has been launched', {})
        self.exchangeInstance.getBalance()
        # at once
        self.getAllMessages()

        # todo: условия что все ок
        while True:
            self.getAllMessages()

            # exchange -> bot
            currentMarketData = self.exchangeInstance.getMarketData('ETH')
            if currentMarketData is None:
                self.sendMessage('ERROR', 'Exchange response error', {})

            currentPrice, currentTime = currentMarketData['price'], currentMarketData['time']
            commonForecast = []
            aggregatedAnswer = None

            # bot -> signal -> bot
            for signal in self.signals:
                signalAnswer = signal.getWeightedForecast(currentTime)
                print(currentPrice, currentTime)
                print(signal.signalName, signalAnswer)
                commonForecast.append(signalAnswer)

            # todo: blockers-modificators (сначала подключаем все? тут просто вызываем)

            aggregatedAnswer = self.aggregateAnswer(commonForecast)
            self.makeDecision(aggregatedAnswer)

            time.sleep(1.01)
            #time.sleep(int(os.environ['SLEEP_DURATION']))

            # если больше уверенности по конфигу - ставим ордер
            # текущий статус и инфу по ордеру держим в кэше, пишем в базу, если упали


x = BotEntrypointClass()
