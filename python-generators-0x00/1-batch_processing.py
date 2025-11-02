#!/usr/bin/env python3
"""
1-batch_processing.py
~~~~~~~~~~~~~~~~~~~~~
Batch processing of user_data with generators.

Objectives:
    1. stream_users_in_batches(batch_size) → yields list of rows in batches
    2. batch_processing(batch_size) → filters age > 25 and prints

Constraints:
    - Use `yield` generator
    - No more than 3 loops in entire file
    - Secure: load config from .env
    - Output: one dict per line (same as 2-main.py)

Security:
    - All DB credentials from .env
    - No secrets in code
"""

import os
from pathlib import Path
from typing import List, Dict, Generator

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# --------------------------------------------------------------------------- #
# Load .env from same directory
# --------------------------------------------------------------------------- #
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "prodev_user"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "ALX_prodev"),
}


# --------------------------------------------------------------------------- #
# 1. Generator: stream_users_in_batches(batch_size)
# --------------------------------------------------------------------------- #
def stream_users_in_batches(batch_size: int) -> Generator[List[Dict], None, None]:
    """
    Fetch users from `user_data` in fixed-size batches using a generator.

    Args:
        batch_size (int): Number of rows per batch.

    Yields:
        list[dict]: Batch of user records (each is a dict).

    Uses:
        - One loop: while True + fetchmany()
    """
    if batch_size <= 0:
        return

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            # Convert age to int if possible
            for row in batch:
                if isinstance(row.get('age'), (int, float)):
                    row['age'] = int(row['age']) if row['age'] == int(row['age']) else row['age']
            yield batch

    except Error as e:
        print(f"Database error in stream_users_in_batches(): {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------------------------------- #
# 2. Process batches: filter age > 25 and print
# --------------------------------------------------------------------------- #
import sys  # for printing to stdout

def batch_processing(batch_size: int) -> None:
    """
    Process user batches: filter users with age > 25 and print one per line.

    Args:
        batch_size (int): Size of each batch to fetch.

    Output:
        Prints dicts to stdout (compatible with `| head -n 5`)
    """
    try:
        for batch in stream_users_in_batches(batch_size):  # ← Loop 1
            for user in batch:                            # ← Loop 2
                if user.get('age', 0) > 25:               # ← age filter
                    print(user)                           # ← prints dict
    except BrokenPipeError:
        # Graceful exit when pipe is closed (e.g., `| head`)
        sys.stderr.close()
