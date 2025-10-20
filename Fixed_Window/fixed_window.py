import time
from collections import defaultdict
import asyncio

class FixedWindowRateLimiter:
    def __init__(self, max_requests, window_seconds, locks):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.user_requests = defaultdict(lambda: {"count": 0, "window_start": time.time()})
        self.locks = locks

    async def allow_request(self, key):
        async with self.locks[key]:
            current_time = time.time()
            data = self.user_requests[key]

            if current_time - data["window_start"] >= self.window_seconds:
                data["count"] = 0
                data["window_start"] = current_time

            data["count"] += 1
            allowed = data["count"] <= self.max_requests

            info = {
                "limit": self.max_requests,
                "remaining": max(0, self.max_requests - data["count"]),
                "reset": int(data["window_start"] + self.window_seconds - current_time)
            }

            return allowed, info

    def reset(self):
        self.user_requests.clear()
