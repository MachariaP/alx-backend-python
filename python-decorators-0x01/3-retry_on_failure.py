import time
import sqlite3
import functools

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

# === Retry Decorator ===
def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function up to 'retries' times
    if it raises any exception. Waits 'delay' seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None

            while attempts < retries:
                try:
                    return func(*args, **kwargs)  # Try to execute
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    if attempts < retries:
                        print(f"Attempt {attempts} failed: {e}. Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed. Giving up.")
            # After all retries, raise the last exception
            raise last_exception
        return wrapper
    return decorator


# === Function with Connection + Retry ===
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# === Test the retry behavior ===
users = fetch_users_with_retry()
print(users)
