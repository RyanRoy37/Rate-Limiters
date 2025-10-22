This repo consists of code, implementing the commonly used Rate-Limiting Algorithms.

# Rate Limiting Algorithms

Rate Limiting Algorithms are mechanisms designed to control the rate at which requests are processed or served by a system. These algorithms are crucial in various domains such as web services, APIs, network traffic management, and distributed systems to ensure stability, fairness, and protection against abuse.

# Types

 - Fixed-Window
 - Sliding-Window
 - Token-Bucket
 - Leaky-Bucket

# Real-World Examples of Rate Limiting

- APIs
- Web Servers
- Content Delivery Networks (CDNs)
- E-commerce Platforms

We will be implementing the algorithms for APIs

## Overview

- APIs are key for cloud apps; exposed to public traffic.
- DoS/DDoS can exhaust resources, making APIs unavailable.

## Threats & Attack Vectors

- Volumetric attacks (high traffic).
- Protocol/network attacks (SYN, UDP floods).
- Application-layer attacks (expensive endpoints, slow requests).
- Resource exhaustion (CPU, memory, DB).
- API abuse & enumeration.
- Attackers’ Goals
- Make API unavailable.
- Increase cloud costs.
- Distract defenders.
- Exploit stressed systems.

## Defense-in-Depth Strategy

- Edge protection (CDN, WAF, DDoS services).
-  ## API Gateway (auth, quotas, throttling).
- Rate limiting & throttling.
- Request validation & size limits.
- Caching & CDNs.
- Queues & async processing.
- Autoscaling & graceful degradation.
- Connection & resource limits.
- Monitoring & automated response.
- Incident response playbook.


 - This FastAPI project demonstrates four types of rate-limiting algorithms—Fixed Window, Sliding Window Counter, Token Bucket, and Leaky Bucket—applied per client. It allows testing and comparing different rate-limiting strategies in an asynchronous web environment.

## Features

Multiple Algorithms:

 - Fixed Window – Limits requests per fixed interval.

 - Sliding Window Counter – Smooths bursts using smaller buckets in a window.

 - Token Bucket – Controls request rate using refillable tokens.

 - Leaky Bucket – Processes requests at a steady rate, preventing spikes.

 - Per-Client Limiting:
Clients are identified by the X-Client-ID header or request IP. Async locks ensure concurrency safety.

## Endpoints:

 - GET / – Basic info and instructions.

 - POST /request or GET /request – Apply rate limiting using query parameter algo. Returns JSON with status, client info, algorithm, and rate-limit metadata.

 - POST /admin/clear – Reset all limiter states (requires header secret: admin-secret).

## Rate-Limit Headers:

 - X-RateLimit-Algorithm
 - X-RateLimit-Limit
 - X-RateLimit-Remaining
 - X-RateLimit-Reset

## Setup

 -Clone the repository:

git clone <your-repo-url>
cd <repo-folder>


 - Install dependencies:

pip install -r requirements.txt


 - Run the server:

uvicorn main:app --reload --port 8000


## Example Requests:

# Using Fixed Window limiter
curl -H "X-Client-ID: user123" "http://localhost:8000/request?algo=fixed_window"

# Clear all limiter states
curl -X POST -H "secret: admin-secret" "http://localhost:8000/admin/clear"

## How It Works

Shared Locks: Each client key has an async lock to handle concurrent requests safely.

Limiter Initialization: Each algorithm is instantiated with parameters like capacity, window duration, and buckets.

## Request Handling:

Extract client key.

Select limiter based on query parameter.

Call allow_request(key) to check if the request is allowed.

Return JSON and rate-limit headers.

This setup is ideal for benchmarking and comparing different rate-limiting strategies in an async web environment.


# Conclusion

Rate limiting is critical for API protection against resource exhaustion and ensuring fair resource allocation. This study compares four rate limiting algorithms—Fixed Window, Leaky Bucket, Sliding Window, and Token Bucket—implemented in FastAPI under realistic load conditions.
Using Apache JMeter, we conducted load tests with 50 concurrent threads, 10-second ramp-up, and 100 iterations against a /request endpoint with algorithm-specific path parameters. Metrics including throughput, success/failure rates, and server hits per second were collected at one-second granularity over 111 seconds.
Results reveal distinct characteristics: Token Bucket demonstrated superior stability with consistent 15-20 transactions/sec throughput and minimal variance, optimal for predictable user experience. Fixed Window showed progressive degradation with increasing failure rates over time due to boundary effects. Sliding Window proved most restrictive with 5:1 failure-to-success ratio at peak load, suitable for high-security scenarios. Leaky Bucket exhibited moderate performance but unpredictable spike patterns.
Recommendations: Token Bucket for consumer-facing services requiring predictable performance, Sliding Window for high-security APIs prioritizing strict enforcement, and avoiding Fixed Window in sustained high-load scenarios. These findings enable data-driven rate limiting strategy selection for production API deployments in microservices architectures and API gateways.