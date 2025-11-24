# Add to services/cache.py
from functools import wraps
import redis
import pickle
import json


# Redis cache for frequently accessed data
def cache_response(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            # Check cache
            cached = redis_client.get(key)
            if cached:
                return pickle.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)
            # Cache result
            redis_client.setex(key, ttl, pickle.dumps(result))
            return result

        return wrapper

    return decorator

