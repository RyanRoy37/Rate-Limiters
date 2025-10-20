from collections import defaultdict
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from typing import Optional, Dict
app = FastAPI(title="Timestamp-based Rate Limiters")
# Import algorithms
from Fixed_Window.fixed_window import FixedWindowRateLimiter
from Sliding_Window.sliding_window import SlidingWindowCounterRateLimiter
from Token_Bucket.token_bucket import TokenBucketRateLimiter
from Leaky_Bucket.leaky_bucket import LeakyBucketRateLimiter



# Shared locks per client key
locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

def get_lock(key: str) -> asyncio.Lock:
    """Get or create a lock for a specific key."""
    if key not in locks:
        locks[key] = asyncio.Lock()
    return locks[key]

# Instantiate limiters
DEFAULT_LIMITERS = {
    "fixed_window": FixedWindowRateLimiter(max_requests=10, window_seconds=60, locks=locks),
    "sliding_counter": SlidingWindowCounterRateLimiter(max_requests=10, window_seconds=60, buckets=6, locks=locks),
    "token_bucket": TokenBucketRateLimiter(capacity=10, window_seconds=60, locks=locks),
    "leaky_bucket": LeakyBucketRateLimiter(capacity=10, window_seconds=60, locks=locks),
}

@app.get("/")
async def root():
    return {"msg": "Rate limiter demo. Use /request?algo=<name> with header X-Client-ID."}

async def get_client_key(request: Request, x_client_id: Optional[str] = Header(None)) -> str:
    """Extract unique client identifier."""
    if x_client_id:
        return x_client_id
    return request.client.host if request.client else "anonymous"

@app.post("/request")
@app.get("/request")
async def handle_request(request: Request, algo: str = "fixed_window", x_client_id: Optional[str] = Header(None)):
    """Main endpoint to process requests and apply rate limiting."""
    key = await get_client_key(request, x_client_id)
    algo = algo.lower()
    limiter = DEFAULT_LIMITERS.get(algo)
    if not limiter:
        raise HTTPException(status_code=400, detail=f"Unknown algorithm '{algo}'. Available: {list(DEFAULT_LIMITERS.keys())}")
    
    allowed, info = await limiter.allow_request(key)
    headers = {
        "X-RateLimit-Algorithm": algo,
        "X-RateLimit-Limit": str(info.get("limit", "-")),
        "X-RateLimit-Remaining": str(info.get("remaining", "-")),
        "X-RateLimit-Reset": str(info.get("reset", "-")),
    }
    status = 200 if allowed else 429
    return JSONResponse(status_code=status, content={"allowed": allowed, "algorithm": algo, "client": key, "info": info}, headers=headers)

@app.post("/admin/clear")
async def clear_all(secret: Optional[str] = Header(None)):
    """Reset all limiter states (for benchmarking)."""
    if secret != "admin-secret":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    for name, limiter in DEFAULT_LIMITERS.items():
        limiter.reset()
    return {"cleared": True}

# Run with: uvicorn main:app --reload --port 8000
