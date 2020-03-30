import time


class RDLock:
    def __init__(self, redisconn, sleeptime=100, prefix='lock_'):
        self.redisconn = redisconn
        self.sleeptime = sleeptime / 1000
        self.prefix = prefix
        self.new_time = None

    def acquire(self, key, expire=5, timeout: int = None):
        """ Acquire a redis distribution lock from redis connection with block mode"""
        if timeout: assert isinstance(timeout, int)
        while True:
            if self.redisconn.set(self.prefix + key, time.time() + expire, nx=True, ex=expire):
                return True
            else:
                current_lock_time = self.redisconn.get(self.prefix + key)
                if current_lock_time:
                    current_lock_time = float(current_lock_time)
                    if time.time() > current_lock_time:
                        new_time = time.time() + expire
                        old_time_var = self.redisconn.getset(self.prefix + key, new_time, ex=expire)
                        if old_time_var == current_lock_time:
                            self.new_time = new_time
                            return True
                if timeout:
                    if timeout <= 0: return False
                    timeout -= self.sleeptime
                time.sleep(self.sleeptime)

    def acquire_no_block(self, key, expire=5):
        """ Acquire a redis distribution lock from redis connection with No-block mode"""
        if self.redisconn.set(self.prefix + key, time.time() + expire, nx=True, ex=expire):
            return True
        else:
            current_lock_time = self.redisconn.get(self.prefix + key)
            if current_lock_time:
                current_lock_time = float(current_lock_time)
                if time.time() > current_lock_time:
                    new_time = time.time() + expire
                    old_time_var = self.redisconn.getset(self.prefix + key, new_time, ex=expire)
                    if old_time_var == current_lock_time:
                        self.new_time = new_time
                        return True
        return False

    def release(self, key):
        if self.new_time:
            if time.time() > self.new_time:
                self.new_time = None
                return
        self.redisconn.delete(self.prefix + key)