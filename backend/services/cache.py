# backend/services/cache.py
from functools import wraps
import pickle
import time
import inspect

# Simple in-memory cache
_in_memory_cache = {}

def cache_response(ttl: int = 300):
    """
    Cache decorator without Redis. Works for both sync and async functions.
    """
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_entry = _in_memory_cache.get(key, None)

            # Check cache and expiry
            if cached_entry:
                value, expire_at = cached_entry
                if time.time() < expire_at:
                    return pickle.loads(value)
                else:
                    del _in_memory_cache[key]

            # Call function
            if inspect.iscoroutinefunction(func):
                # async function
                async def async_call():
                    result = await func(*args, **kwargs)
                    _in_memory_cache[key] = (pickle.dumps(result), time.time() + ttl)
                    return result
                return async_call()
            else:
                # sync function
                result = func(*args, **kwargs)
                _in_memory_cache[key] = (pickle.dumps(result), time.time() + ttl)
                return result

        return sync_wrapper
    return decorator
