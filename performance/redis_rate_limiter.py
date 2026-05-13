import redis
import time

class RedisRateLimiter:

    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port)

    def check(self, key, limit=300, window=60):

        current = int(time.time())
        bucket = f"rate:{key}:{current // window}"

        count = self.redis.incr(bucket)

        if count == 1:
            self.redis.expire(bucket, window)

        if count > limit:
            raise Exception("Rate limit exceeded")
