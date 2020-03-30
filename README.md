## Redis Distributed Lock
Redis distributed lock for python3, using setnx and getset, 
provide block and no-block function
### Install
```
pip install redis-distributed-lock
```
### Usage
```
from redis_distributed_lock import RDLock

lock = RDLock(redisconn)

# Specify the sleeptime for block mode (default 100 millsec)
lock = RDLock(redisconn, sleeptime=1000)

# Specify lock prefix name (default: lock_)
lock = RDLock(redisconn, prefix="lock_")

# Using block method, default timeout is none, default key expire is 5 sec
try:
    if lock.acquire(key, expire=5, timeout=2):
        # Do something
finally:
    lock.release()

# Using No-block method
lock.acquire_no_block(key)
```