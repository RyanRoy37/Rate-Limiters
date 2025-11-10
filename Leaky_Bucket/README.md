Leaky Bucket Rate Limiter

The Leaky Bucket Rate Limiter is a mechanism to control the rate of requests over time, smoothing out bursts. Unlike fixed windows, it allows occasional bursts as long as the average request rate does not exceed the defined limit.

How It Works

Bucket Concept:
Each client has a "bucket" that holds tokens representing requests. The bucket has a capacity, which is the maximum number of requests it can hold.

Leaking Tokens:
Tokens leak out of the bucket at a constant rate (calculated as capacity / window_seconds). This ensures the request rate is smoothed over time.

Processing Requests:

When a request arrives, the algorithm calculates how many tokens have leaked since the last request.

It removes leaked tokens from the bucket.

If the bucket is not full (tokens < capacity), the request is allowed and a token is added.

If the bucket is full, the request is rejected.

Response Information:
For each request, it provides:

allowed: Whether the request can proceed.

limit: Maximum bucket capacity.

remaining: Available tokens in the bucket.

reset: Time in seconds until the bucket has space for a new request.

Working in the Above Code

__init__: Initializes the limiter with the bucket capacity, time window, and async locks for concurrency.

allow_request:

Acquires the lock for the user key.

Updates the bucket by subtracting tokens that leaked since the last request.

Checks if there is space in the bucket; if yes, increments tokens and allows the request.

Returns allowed status and request info.

reset: Clears all bucket data, starting fresh for all users.