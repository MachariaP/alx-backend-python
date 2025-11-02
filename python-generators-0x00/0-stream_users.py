#!/usr/bin/env python3
"""
0-stream_users.py
~~~~~~~~~~~~~~~~~
Generator that streams rows from the `user_data` table one at a time.

Objective:
    Create a generator function `stream_users()` that yields user records
    as dictionaries using Python's `yield` keyword.

Constraints:
    - Must use a generator (yield)
    - Only one loop allowed
    - Output format: dict with keys: user_id, name, email, age
    - Must work with 1-main.py using islice()

Security:
    - All DB credentials loaded from `.env`
    - No hardcoded secrets
"""

import os
from pathlib import Path
from typing import Dict, Generator

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# --------------------------------------------------------------------------- #
# Load environment variables from .env (same directory)
# --------------------------------------------------------------------------- #
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

# Database configuration from .env
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "prodev_user"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "prodev_db"),
}


# --------------------------------------------------------------------------- #
# Generator: stream_users()
# --------------------------------------------------------------------------- #
def stream_users() -> Generator[Dict[str, object], None, None]:
    """
    Generator that yields one user record at a time from the `user_data` table.

    Each yielded value is a dictionary:
        {
            'user_id': str (UUID),
            'name': str,
            'email': str,
            'age': int or float
        }

    Uses a single loop with `fetchone()` and `yield` to stream rows efficiently.

    Yields:
        dict: One user record per iteration.

    Raises:
        Stops gracefully on database errors (prints error and stops yielding).
    """
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)  # Return rows as dicts
        cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id")

        # SINGLE LOOP: fetch one row at a time
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            # Convert age to int if it's a Decimal
            if 'age' in row and isinstance(row['age'], (float, int)):
                row['age'] = int(row['age']) if row['age'] == int(row['age']) else row['age']
            yield row

    except Error as e:
        print(f"Database error in stream_users(): {e}")
    except Exception as e:
        print(f"Unexpected error in stream_users(): {e}")
    finally:
        # Always close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test standalone)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     from itertools import islice
#     for user in islice(stream_users(), 6):
#         print(user)
