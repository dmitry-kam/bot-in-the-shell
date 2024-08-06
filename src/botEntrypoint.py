from redis import StrictRedis
import importlib
import datetime
import orjson
import redis
import time
import os

class BotEntrypointClass():
    # Singleton pattern
    botInstance = None

    # attributes
    exchangeInstance = None
    cache = None
    redisSubscriber = None
    loggers = []
    signals = []

    def __new__(cls, *args, **kwargs):
        if cls.botInstance is None:
            cls.botInstance = object.__new__(cls, *args, **kwargs)
        return cls.botInstance

    def __init__(self):
        self.initCache()
        self.initExchange()
        self.setLoggers()
        
        self.startBot()

    def initCache(self):
        self.cache = StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)
        
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

        self.redisSubscriber = self.cache.pubsub()
        self.redisSubscriber.psubscribe(**{'logs': self.handleLogMessage})

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
        module = importlib.import_module('signalX.' + os.environ['SIGNAL_HANDLER'])
        # signalClass = getattr(module, os.environ['SIGNAL_HANDLER'])
        # signalInstance = signalClass()
        # signalInstance.move()

    def selfCheck(self):
        # todo каждый час
        print('selfCheck')

    def startBot(self):
        now = datetime.datetime.now()
        startMessage = {
            "level": "OK",
            "message": "Bot has been launched",
            "context": {},
            "time": str(now)
        }
        self.cache.publish('logs', orjson.dumps(startMessage))

        # todo: условия что все ок
        while True:
            self.redisSubscriber.get_message()

            time.sleep(3)
            #time.sleep(int(os.environ['SLEEP_DURATION']))


x = BotEntrypointClass()

# self.cache.set('timeY', time.time())
# self.exchangeInstance.getBalance()