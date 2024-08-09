from redis import StrictRedis
import datetime
import orjson
import os


class RedisCustom():
    cacheInstance = None
    redisConnection = None
    logsChannel = 'logs'

    def __new__(cls, *args, **kwargs):
        if cls.cacheInstance is None:
            cls.cacheInstance = object.__new__(cls, *args, **kwargs)
        return cls.cacheInstance

    def __init__(self):
        print('Init cache')
        self.redisConnection = StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

    def now(self):
        now = datetime.datetime.now()
        return str(now)

    def getMessageString(self, level: str, message: str, context: dict):
        return orjson.dumps(self.getMessageObject(level, message, context))

    def getMessageObject(self, level: str, message: str, context: dict):
        return {
            "level": level,
            "message": message,
            "context": context,
            "time": self.now()
        }

    def sendMessage(self, level: str, message: str, context: dict):
        self.redisConnection.publish(self.logsChannel, self.getMessageString(level, message, context))

    def setKeyValue(self, key, value):
        self.redisConnection.set(key, value)
    def getKeyValue(self, key):
        self.redisConnection.get(key)

