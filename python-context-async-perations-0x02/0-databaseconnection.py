#!/usr/bin/env python3
"""
0-databaseconnection.py

Demonstrates a **custom class-based context manager** for SQLite database
connections. It automatically opens a connection, provides a cursor,
commits on success, rolls back on error, and always closes the connection.

"""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    A class-based context manager for SQLite database connections.

    Ensures:
    - Connection is opened in __enter__
    - Cursor is available via `self.cursor`
    - Transaction is committed on success
    - Transaction is rolled back on exception
    - Connection is always closed in __exit__

    Usage:
        with DatabaseConnection('mydb.sqlite') as db:
            db.cursor.execute("SELECT * FROM users")
            print(db.cursor.fetchall())
    """

    def __init__(self, db_path: str):
        """
        Initialize with the path to the SQLite database file.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path: str = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self):
        """
        Enter the runtime context.
        Opens the connection, creates a cursor, and returns self.

        Returns:
            DatabaseConnection: The instance with active connection and cursor.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Optional: nicer dict-like rows
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
            return self
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context.
        Commits if no error, rolls back if error occurred, then closes.

        Args:
            exc_type: Exception class (or None)
            exc_value: Exception instance (or None)
            traceback: Traceback object (or None)

        Returns:
            bool: False (let exceptions propagate)
        """
        if self.conn:
            if exc_type is None:
                # No exception → commit
                try:
                    self.conn.commit()
                    print("Transaction committed.")
                except sqlite3.Error as e:
                    print(f"Commit failed: {e}")
                    self.conn.rollback()
            else:
                # Exception occurred → rollback
                try:
                    self.conn.rollback()
                    print(f"Transaction rolled back due to: {exc_value}")
                except sqlite3.Error as e:
                    print(f"Rollback failed: {e}")

            # Always close connection
            try:
                self.conn.close()
                print("Database connection closed.")
            except sqlite3.Error as e:
                print(f"Error closing connection: {e}")

        return False  # Do not suppress exceptions


# ————————————————————————————————————————————————————————————————
# Demo: Create a sample DB, insert data, and query using the context manager
# ————————————————————————————————————————————————————————————————

def create_sample_db(db_path: str = "users.db") -> None:
    """Create a sample 'users' table and insert dummy data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)
    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
        [
            ("Alice", "alice@example.com"),
            ("Bob", "bob@example.com"),
            ("Charlie", "charlie@example.com"),
        ]
    )
    conn.commit()
    conn.close()
    print(f"Sample database created at: {db_path}")


def main() -> None:
    """Main demo using the DatabaseConnection context manager."""
    db_file = "users.db"

    # Step 1: Create sample database
    create_sample_db(db_file)

    # Step 2: Use context manager to query
    print("\nQuerying users table...")
    try:
        with DatabaseConnection(db_file) as db:
            db.cursor.execute("SELECT * FROM users")
            rows = db.cursor.fetchall()

            if rows:
                print("\nUsers found:")
                for row in rows:
                    # Works with row_factory = sqlite3.Row
                    print(f"  ID: {row['id']}, Name: {row['name']}, Email: {row['email']}")
            else:
                print("No users found.")
    except Exception as e:
        print(f"Query failed: {e}")


if __name__ == "__main__":
    main()
