
import time
import functools


def ttl_cache(seconds):

    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds <= 0:
        raise ValueError("Cache time must be positive")

    def decorator(function):

        cache = {}
        hits = 0
        misses = 0

        @functools.wraps(function)
        def wrapper(*args, **kwargs):

            nonlocal hits, misses

            # Create a consistent cache key
            try:
                key = (args, tuple(sorted(kwargs.items())))
                hash(key)

            except TypeError:
                # Unhashable arguments are not cached
                misses += 1
                return function(*args, **kwargs)

            current_time = time.monotonic()

            # Check cache
            if key in cache:

                result, saved_time = cache[key]

                if current_time - saved_time < seconds:
                    hits += 1
                    return result

                del cache[key]

            # Calculate new result
            misses += 1

            result = function(*args, **kwargs)

            cache[key] = (result, time.monotonic())

            return result

        # Show cache statistics
        def cache_info():

            return {
                "hits": hits,
                "misses": misses
            }

        wrapper.cache_info = cache_info

        return wrapper

    return decorator


# Example function
@ttl_cache(seconds=5)
def add_numbers(x, y):

    print("Calculating...")
    return x + y


# Test cache
print(add_numbers(x=2, y=3))
print(add_numbers(y=3, x=2))

print(add_numbers.cache_info())
