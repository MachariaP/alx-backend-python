#!/usr/bin/env python3
"""
2-lazy_paginate.py
~~~~~~~~~~~~~~~~~~
Lazy pagination of user_data using a generator.

Objective:
    Implement lazy_paginate(page_size) that yields pages of users
    only when needed, using paginate_users(page_size, offset).

Constraints:
    - Only one loop in the generator
    - Use `yield`
    - Include `paginate_users()` function
    - Secure: load config from .env
"""

import os
import sys
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
    "database": os.getenv("MYSQL_DATABASE", "prodev_db"),
}


# --------------------------------------------------------------------------- #
# Helper: paginate_users(page_size, offset)
# --------------------------------------------------------------------------- #
def paginate_users(page_size: int, offset: int) -> List[Dict]:
    """
    Fetch one page of users from `user_data` using LIMIT/OFFSET.

    Args:
        page_size (int): Number of rows per page.
        offset (int): Starting row offset.

    Returns:
        list[dict]: List of user records (empty if no more rows).
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        query = (
            "SELECT user_id, name, email, age "
            "FROM user_data ORDER BY user_id "
            "LIMIT %s OFFSET %s"
        )
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()

        # Normalise age to int when possible
        for row in rows:
            age = row.get("age")
            if isinstance(age, (int, float)):
                row["age"] = int(age) if age == int(age) else age

        return rows

    except Error as e:
        print(f"Database error in paginate_users(): {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------------------------------- #
# Generator: lazy_paginate(page_size)
# --------------------------------------------------------------------------- #
def lazy_paginate(page_size: int) -> Generator[List[Dict], None, None]:
    """
    Lazily yield pages of users from the database.

    Only fetches the next page when the current one is exhausted.
    Starts at offset 0 and increments by `page_size`.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list[dict]: One page of user records.
    """
    if page_size <= 0:
        return

    offset = 0
    while True:                     # ← **ONLY ONE LOOP**
        page = paginate_users(page_size, offset)
        if not page:                # no more rows → stop
            break
        yield page
        offset += page_size


# --------------------------------------------------------------------------- #
# Export name expected by 3-main.py
# --------------------------------------------------------------------------- #
lazy_pagination = lazy_paginate
