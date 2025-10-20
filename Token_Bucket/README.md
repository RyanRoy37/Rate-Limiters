Token Bucket Rate Limiter

The Token Bucket Rate Limiter is a popular algorithm for controlling request rates while allowing short bursts of traffic. It uses a “bucket” of tokens to represent available request capacity.

How It Works

Bucket and Tokens:
Each client has a bucket with a fixed capacity representing the maximum number of requests it can make immediately. Each request consumes a token.

Token Refill:
Tokens are replenished over time at a constant refill rate (calculated as capacity / window_seconds). This ensures the system allows a smooth request rate over time while accommodating bursts up to the bucket capacity.

Processing Requests:

When a request arrives, the algorithm refills tokens based on elapsed time since the last request.

If the bucket has at least one token, the request is allowed and a token is removed.

If no tokens are available, the request is rejected.

Response Information:
For each request, it returns:

allowed: Whether the request can proceed.

limit: Maximum token capacity.

remaining: Tokens left in the bucket.

reset: Estimated time until a new token is available if the bucket is empty.

Working in the Above Code

__init__: Initializes the limiter with bucket capacity, refill rate, and async locks for safe concurrency.

allow_request:

Acquires the lock for the user key.

Refills tokens based on elapsed time.

Checks if a token is available; if yes, decrements it and allows the request.

Returns allowed status and info dictionary.

reset: Clears all token buckets, starting fresh for all users.