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

# === Transaction Management Decorator ===
def transactional(func):
    """
    Ensures the function runs inside a transaction.
    - Commits if no error
    - Rolls back if an exception occurs
    Must be used with @with_db_connection
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Start transaction (implicit with sqlite3)
            result = func(conn, *args, **kwargs)
            conn.commit()        # Success → save changes
            return result
        except Exception as e:
            conn.rollback()      # Error → undo changes
            print(f"Transaction rolled back due to: {e}")
            raise                # Re-raise the error
    return wrapper


# === Example Function with Both Decorators ===
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    # No commit/rollback here — handled by @transactional


# === Test the function ===
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
