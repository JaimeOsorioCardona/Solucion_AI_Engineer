"""
Redis Caching Solution.

This module demonstrates how to implement a Redis cache decorator to optimize
endpoints with high read frequency and heavy database queries.

## Cache Flow Diagram (Mermaid.js)

```mermaid
flowchart TD
    A[Request to /api/routes] --> B{Check Redis Cache}
    B -- Cache HIT --> C[Return Cached Response]
    B -- Cache MISS --> D[Query Database]
    D --> E[Store Result in Redis with TTL]
    E --> F[Return Fresh Response]

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
    style D fill:#ff9,stroke:#333,stroke-width:2px
    style E fill:#9cf,stroke:#333,stroke-width:2px
```
"""

import functools
import json
import time
from typing import Any, Callable, Optional

# Mock Redis client for demonstration (with TTL support)
class MockRedis:
    def __init__(self):
        self.cache: dict[str, tuple[str, float]] = {}  # key -> (value, expiry_timestamp)

    def get(self, name: str) -> Optional[str]:
        entry = self.cache.get(name)
        if entry is None:
            return None
        value, expiry = entry
        if expiry and time.time() > expiry:
            del self.cache[name]
            return None
        return value

    def set(self, name: str, value: str, ex: int = 0) -> None:
        expiry = time.time() + ex if ex > 0 else 0
        self.cache[name] = (value, expiry)

redis_client = MockRedis()

def cache_response(ttl_seconds: int = 300):
    """
    Decorator to cache the result of a function in Redis.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate a unique cache key based on function name and arguments
            # In a real app, ensure args are serializable or use a specific key strategy
            key_part = json.dumps([args, kwargs], sort_keys=True)
            cache_key = f"{func.__name__}:{key_part}"
            
            # 1. Check Cache
            cached_value = redis_client.get(cache_key)
            if cached_value:
                print(f"Cache Hit for {cache_key}!")
                return json.loads(cached_value)
            
            # 2. If Miss, Execute Function
            print(f"Cache Miss for {cache_key}. Querying DB...")
            result = func(*args, **kwargs)
            
            # 3. Store in Cache
            redis_client.set(cache_key, json.dumps(result), ex=ttl_seconds)
            
            return result
        return wrapper
    return decorator

# --- Example Usage ---

@cache_response(ttl_seconds=60)
def get_routes(user_id: int):
    """
    Simulates fetching routes from a database.
    """
    # Simulate DB Latency
    time.sleep(1) 
    return {"user_id": user_id, "routes": ["Route A", "Route B"]}

if __name__ == "__main__":
    print("--- First Call (Cold Cache) ---")
    start = time.time()
    print(get_routes(123))
    print(f"Time: {time.time() - start:.4f}s")
    
    print("\n--- Second Call (Warm Cache) ---")
    start = time.time()
    print(get_routes(123))
    print(f"Time: {time.time() - start:.4f}s")
