#!/usr/bin/env python3
"""
seed.py
~~~~~~~~
Database seeding module for the ALX ProDev backend project.

This module provides functions to:
  • Connect to MySQL server
  • Create the target database (if missing)
  • Connect to the created database
  • Create the `user_data` table (idempotent)
  • Insert rows from a CSV file with UUID primary keys

All credentials are loaded from a `.env` file — **no secrets in code**.

Requirements:
    pip install mysql-connector-python python-dotenv
"""

import os
import uuid
import csv
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection

# --------------------------------------------------------------------------- #
# Load environment variables from .env (in the same directory as this file)
# --------------------------------------------------------------------------- #
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

# All configuration comes from environment — defaults are safe fallbacks
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "prodev_db"),  # <-- DB name from .env
}


# --------------------------------------------------------------------------- #
# 1. Connect to MySQL server (no database selected)
# --------------------------------------------------------------------------- #
def connect_db() -> Optional[MySQLConnection]:
    """
    Establish a connection to the MySQL server without selecting a database.

    Returns:
        MySQLConnection object or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"],
        )
        print("Connected to MySQL server.")
        return conn
    except Error as e:
        print(f"Failed to connect to MySQL server: {e}")
        return None


# --------------------------------------------------------------------------- #
# 2. Create database if it does not exist
# --------------------------------------------------------------------------- #
def create_database(connection: MySQLConnection) -> None:
    """
    Create the target database if it does not already exist.

    Args:
        connection: Active connection to MySQL server (no DB selected).
    """
    if not connection or not connection.is_connected():
        print("Invalid connection for create_database()")
        return

    db_name = DB_CONFIG["database"]
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        print(f"Database `{db_name}` ensured.")
        cursor.close()
    except Error as e:
        print(f"Error creating database `{db_name}`: {e}")


# --------------------------------------------------------------------------- #
# 3. Connect to the specific database (prodev_db)
# --------------------------------------------------------------------------- #
def connect_to_prodev() -> Optional[MySQLConnection]:
    """
    Connect to the `prodev_db` database using credentials from .env.

    Returns:
        MySQLConnection object or None on failure.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"Connected to database `{DB_CONFIG['database']}`.")
        return conn
    except Error as e:
        print(f"Failed to connect to `{DB_CONFIG['database']}`: {e}")
        return None


# --------------------------------------------------------------------------- #
# 4. Create table `user_data` if it does not exist
# --------------------------------------------------------------------------- #
def create_table(connection: MySQLConnection) -> None:
    """
    Create the `user_data` table with proper schema (idempotent).

    Schema:
        user_id  CHAR(36)   PRIMARY KEY   (UUID)
        name     VARCHAR(255) NOT NULL
        email    VARCHAR(255) NOT NULL
        age      DECIMAL(5,2) NOT NULL
        INDEX on email

    Args:
        connection: Active connection to the target database.
    """
    if not connection or not connection.is_connected():
        print("Invalid connection for create_table()")
        return

    create_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX idx_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_sql)
        print("Table `user_data` created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


# --------------------------------------------------------------------------- #
# 5. Insert CSV data with UUIDs (skip duplicates & invalid rows)
# --------------------------------------------------------------------------- #
def insert_data(connection: MySQLConnection, csv_filename: str) -> None:
    """
    Read a CSV file and insert rows into `user_data`.

    - Generates a UUID for each row
    - Uses `INSERT IGNORE` → skips duplicate primary keys
    - Skips rows with missing/invalid fields
    - Commits only once at the end

    Expected CSV header:
        "name","email","age"

    Args:
        connection: Active connection to the database.
        csv_filename: Path to CSV file (relative or absolute).
    """
    if not connection or not connection.is_connected():
        print("Invalid connection for insert_data()")
        return

    csv_path = Path(csv_filename)
    if not csv_path.is_file():
        print(f"CSV file not found: {csv_path}")
        return

    insert_sql = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    inserted = 0
    skipped = 0

    try:
        cursor = connection.cursor()
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()
                age_str = row.get("age", "").strip()

                if not (name and email and age_str):
                    skipped += 1
                    continue

                try:
                    age = float(age_str)
                except ValueError:
                    skipped += 1
                    continue

                uid = str(uuid.uuid4())
                cursor.execute(insert_sql, (uid, name, email, age))
                inserted += 1

        connection.commit()
        print(f"Inserted {inserted} rows, skipped {skipped} invalid/duplicates.")
        cursor.close()
    except Error as e:
        print(f"Database error during insert: {e}")
    except Exception as e:
        print(f"Unexpected error reading CSV: {e}")