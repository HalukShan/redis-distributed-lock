import time
import uuid


class RDLock:
    def __init__(self, redisconn, sleeptime=100, prefix='lock_'):
        self.redisconn = redisconn
        self.sleeptime = sleeptime / 1000
        self.prefix = prefix
        self.value = str(uuid.uuid1())
        self.script = """
                    if redis.call('get', KEYS[1]) == ARGV[1] then
                        return redis.call('del', KEYS[1])
                    else
                        return 0
                    end
                """

    def acquire(self, key, expire=5000, timeout: int = None):
        """ Acquire a redis distribution lock from redis connection with block mode
        :param
            expire: int
                key expire time (millisecond)
            timeout: int
                before timeout, keep trying (second)
        """
        if timeout: assert isinstance(timeout, int)
        while True:
            if self.redisconn.set(self.prefix + key, self.value, nx=True, px=expire):
                return True
            if timeout:
                if timeout <= 0: return False
                timeout -= self.sleeptime
            time.sleep(self.sleeptime)

    def acquire_no_block(self, key, expire=5000):
        """ Acquire a redis distribution lock from redis connection with No-block mode"""
        if self.redisconn.set(self.prefix + key, self.value, nx=True, px=expire):
            return True
        else:
            return False

    def release(self, key):
        script = self.redisconn.register_script(self.script)
        script(keys=[self.prefix + key], args=[self.value])
