import time
from collections import defaultdict
import asyncio

class LeakyBucketRateLimiter:
    def __init__(self, capacity, window_seconds, locks):
        self.capacity = capacity
        self.rate = capacity / window_seconds
        self.bucket = defaultdict(lambda: {"tsokens": 0, "last_check": time.time()})
        self.locks = locks

    async def allow_request(self, key):
        async with self.locks[key]:
            now = time.time()
            state = self.bucket[key]
            elapsed = now - state["last_check"]
            state["last_check"] = now

            leaked = elapsed * self.rate
            state["tokens"] = max(0, state["tokens"] - leaked)

            allowed = state["tokens"] < self.capacity
            if allowed:
                state["tokens"] += 1

            info = {
                "limit": self.capacity,
                "remaining": max(0, self.capacity - state["tokens"]),
                "reset": int(self.capacity / self.rate - state["tokens"] / self.rate)
            }

            return allowed, info

    def reset(self):
        self.bucket.clear()
