import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

def log_queries(func):
    """
    Decorator that logs the SQL query before executing the decorated function.
    Assume the function takes a 'query' parameter (positional or keyword).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get current time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract the query from args or kwargs
        query = None
        if args:
            query = args[0] # First positional argument
        elif 'query' in kwargs:
            query = kwargs['query']

        if query:
            print(f"[{now}] Executing query: {query}")
        else:
            print(f"[{now}] Warning: No query found in function arguments.")

        # Execute the original function
        return func(*args, **kwargs)

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query

users = fetch_all_users(query="SELECT * FROM users")
