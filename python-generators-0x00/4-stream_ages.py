#!/usr/bin/env python3
"""
4-stream_ages.py
~~~~~~~~~~~~~~~~
Memory-efficient average age calculation using generators.

Objective:
    - stream_user_ages(): yields ages one-by-one
    - calculate_average_age(): computes average without loading all data
    - Print: "Average age of users: X.XX"
    - No SQL AVG(), only 2 loops total

Security:
    - All DB credentials from .env
    - No secrets in code
"""

import os
import sys
from pathlib import Path
from typing import Generator

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
# 1. Generator: stream_user_ages()
# --------------------------------------------------------------------------- #
def stream_user_ages() -> Generator[float, None, None]:
    """
    Yield user ages one at a time from the `user_data` table.

    Uses cursor.fetchone() → memory efficient (streams 1 row at a time).

    Yields:
        float: age of each user (converted from DECIMAL)

    Raises:
        Stops gracefully on errors.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data ORDER BY user_id")

        # LOOP 1: fetch one row at a time
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            age = row[0]
            # Convert Decimal to float
            yield float(age)

    except Error as e:
        print(f"Database error in stream_user_ages(): {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------------------------------- #
# 2. Calculate average age using the generator
# --------------------------------------------------------------------------- #
def calculate_average_age() -> None:
    """
    Compute and print the average age using streamed ages.

    Uses running sum and count → O(1) memory.
    No SQL AVG(), no list storage.
    """
    total_age = 0.0
    count = 0

    try:
        # LOOP 2: consume the generator
        for age in stream_user_ages():
            total_age += age
            count += 1

        if count == 0:
            print("Average age of users: 0.00")
            return

        average = total_age / count
        print(f"Average age of users: {average:.2f}")

    except Exception as e:
        print(f"Error calculating average: {e}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Run when executed directly
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    calculate_average_age()
