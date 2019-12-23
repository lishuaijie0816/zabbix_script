import time
import redis
from redis.sentinel import Sentinel


sentinel = Sentinel(
    [('192.168.0.2', 26379)],
)
try:
    redis_conn = sentinel.master_for('storage', socket_timeout=3, redis_class=redis.Redis)
    before_timestamp = redis_conn.get('health_check')
    redis_conn.set('health_check', time.time())
    current_timetamp = redis_conn.get(('health_check'))
    if before_timestamp is not None and current_timetamp > before_timestamp:
        print 1
    elif before_timestamp is None: # for the first check
        print 1
    else:
        print 0
except Exception:
    print 0

