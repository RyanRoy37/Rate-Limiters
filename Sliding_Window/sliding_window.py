import time
from collections import defaultdict
import asyncio

class SlidingWindowCounterRateLimiter:
    def __init__(self, max_requests, window_seconds, buckets, locks):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.buckets = buckets
        self.user_buckets = defaultdict(lambda: [0] * buckets)
        self.last_access = defaultdict(lambda: time.time())
        self.locks = locks

    async def allow_request(self, key):
        async with self.locks[key]:
            now = time.time()
            elapsed = now - self.last_access[key]
            bucket_duration = self.window_seconds / self.buckets

            if elapsed > bucket_duration:
                shift = int(elapsed // bucket_duration)
                for _ in range(min(shift, self.buckets)):
                    self.user_buckets[key].pop(0)
                    self.user_buckets[key].append(0)
                self.last_access[key] = now

            total = sum(self.user_buckets[key])
            allowed = total < self.max_requests

            if allowed:
                self.user_buckets[key][-1] += 1

            info = {
                "limit": self.max_requests,
                "remaining": max(0, self.max_requests - total),
                "buckets": list(self.user_buckets[key]),
                "reset": int(bucket_duration)
            }

            return allowed, info

    def reset(self):
        self.user_buckets.clear()
        self.last_access.clear()
