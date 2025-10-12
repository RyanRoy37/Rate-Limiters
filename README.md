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
