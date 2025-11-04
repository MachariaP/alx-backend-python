import time
import sqlite3
import functools

# Global cache to store query results
query_cache = {}

# === Reusable DB Connection Decorator (from Task 1) ===
def with_db_connection(func):
    """Opens DB connection, passes it to function, and closes it."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Cache Query Decorator ===
def cache_query(func):
    """
    Decorator that caches the result of a database query
    using the SQL query string as the cache key.
    """
    @functools.wraps(func)
    def wrapper(conn, query):
        # Use the query string as the cache key
        if query in query_cache:
            print(f"Cache HIT for query: {query}")
            return query_cache[query]
        else:
            print(f"Cache MISS for query: {query} – executing...")
            result = func(conn, query)
            query_cache[query] = result  # Store in cache
            return result
    return wrapper


# === Function with Connection + Cache ===
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# === Test the caching behavior ===
print("=== First call (executes query) ===")
users = fetch_users_with_cache(query="SELECT * FROM users")

print("\n=== Second call (uses cache) ===")
users_again = fetch_users_with_cache(query="SELECT * FROM users")

# Optional: prove they are the same object
print(f"\nSame result object? {users is users_again}")
