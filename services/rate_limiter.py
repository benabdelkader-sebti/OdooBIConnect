import time

class RateLimiter:

    def __init__(self):
        self.requests = {}

    def check(self, key, limit=100):
        now = time.time()
        window = 60

        if key not in self.requests:
            self.requests[key] = []

        self.requests[key] = [
            t for t in self.requests[key] if now - t < window
        ]

        if len(self.requests[key]) >= limit:
            raise Exception("Rate limit exceeded")

        self.requests[key].append(now)
