import time
from collections import defaultdict
import asyncio

class TokenBucketRateLimiter:
    def __init__(self, capacity, window_seconds, locks):
        self.capacity = capacity
        self.refill_rate = capacity / window_seconds
        self.bucket = defaultdict(lambda: {"tokens": capacity, "last_refill": time.time()})
        self.locks = locks

    async def allow_request(self, key):
        async with self.locks[key]:
            now = time.time()
            data = self.bucket[key]
            elapsed = now - data["last_refill"]

            # refill tokens
            refill = elapsed * self.refill_rate
            data["tokens"] = min(self.capacity, data["tokens"] + refill)
            data["last_refill"] = now

            if data["tokens"] >= 1:
                data["tokens"] -= 1
                allowed = True
            else:
                allowed = False

            info = {
                "limit": self.capacity,
                "remaining": int(data["tokens"]),
                "reset": int((1 - data["tokens"]) / self.refill_rate if data["tokens"] < 1 else 0)
            }

            return allowed, info

    def reset(self):
        self.bucket.clear()
