Fixed Window Rate Limiter

A Fixed Window Rate Limiter is a rate-limiting algorithm used to control the number of requests a client can make to a service within a fixed time window. It ensures that a user cannot exceed a predefined number of requests in a specific interval, helping prevent abuse or overloading of the system.

How It Works

Tracking Requests:
Each client (identified by a unique key) has an associated counter and a window start timestamp.

Window Reset:
When a request comes in, the algorithm checks if the current time has exceeded the window duration.

If yes, it resets the counter and updates the window start to the current time.

Counting Requests:
Each incoming request increments the counter. If the counter exceeds the allowed maximum, the request is rejected.

Response Information:
For each request, the algorithm returns:

allowed: Whether the request can proceed.

limit: Maximum allowed requests per window.

remaining: How many requests are left in the current window.

reset: Seconds until the window resets.

Working in the Above Code

__init__: Initializes the limiter with a maximum request count, window duration, and a dictionary of async locks for thread safety.

allow_request:

Acquires the lock for the user key to ensure safe updates.

Checks if the current window has expired; if so, resets the count and window start.

Increments the request count and determines if the request is allowed.

Returns allowed and the info dictionary with request stats.

reset: Clears all user request data, effectively starting fresh.