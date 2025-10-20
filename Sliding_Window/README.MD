Sliding Window Rate Limiter

The Sliding Window is an advanced rate-limiting algorithm that improves upon fixed windows by reducing burstiness near window boundaries. It allows a more precise control over request rates within a sliding time frame.

How It Works

Window Slicing:
The total window duration is divided into smaller buckets. Each bucket tracks the number of requests in its interval.

Sliding the Window:
When a request arrives, the algorithm calculates how many buckets have passed since the last access and shifts the window accordingly. Old bucket counts are dropped, and new buckets start at zero.

Counting Requests:

The algorithm sums the counts across all buckets to get the total requests in the current sliding window.

If the total is below the maximum allowed requests, the request is allowed and the count in the current bucket is incremented.

Otherwise, the request is rejected.

Response Information:
For each request, it provides:

allowed: Whether the request can proceed.

limit: Maximum allowed requests in the full window.

remaining: How many requests are left in the current window.

buckets: Current request counts in each bucket.

reset: Duration of one bucket (helps estimate when the window will shift).

Working in the Above Code

__init__: Sets up the limiter with maximum requests, window duration, number of buckets, and async locks for concurrency safety.

allow_request:

Acquires the lock for the user key.

Determines how many buckets have passed since the last request and shifts the sliding window accordingly.

Sums requests in the current window to check if the new request can be allowed.

Updates the current bucket if allowed and returns request info.

reset: Clears all user data and bucket states, effectively starting fresh.