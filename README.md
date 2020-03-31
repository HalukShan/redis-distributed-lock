## Redis Distributed Lock
Redis distributed lock for python3, using setnx and lua script, 
provide block and no-block function
### Install
```
pip install redis-distributed-lock
```
### Usage
```python
from redis_distributed_lock import RDLock
import redis

redisconn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
lock = RDLock(redisconn)

# Prevent CPU consumption all the time, 
# specify the sleeptime for block mode (default 100 millsec)
lock = RDLock(redisconn, sleeptime=1000)

# Specify lock prefix name (default: lock_)
lock = RDLock(redisconn, prefix="lock_")

# Using block method, default timeout is 0 (second)
# default key expire is 5000 millsec
key = "key"
try:
    if lock.acquire(key, expire=3000, timeout=2):
        # Do something
        pass
finally:
    lock.release(key)

# Using No-block method
lock.acquire_no_block(key)
```