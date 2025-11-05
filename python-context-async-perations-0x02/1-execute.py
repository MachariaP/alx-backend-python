#!/usr/bin/env python3
"""
1-execute.py

Reusable class-based context manager `ExecuteQuery` that:
- Takes a SQL query and parameters
- Opens a database connection
- Executes the query
- Returns the cursor (so results can be fetched)
- Commits/rolls back and closes connection automatically

Directory: python-context-async-perations-0x02
GitHub:    alx-backend-python
"""

import sqlite3
from typing import Any, Tuple, List, Optional


class ExecuteQuery:
    """
    A reusable context manager for executing a parameterized SQL query.

    Features:
    - Accepts any SELECT query and parameters
    - Opens connection in __enter__
    - Executes query and returns cursor for fetching
    - Handles commit/rollback and connection close in __exit__
    - Reusable for any query

    Example:
        with ExecuteQuery(
            "SELECT * FROM users WHERE age > ?",
            (25,)
        ) as cursor:
            results = cursor.fetchall()
    """

    def __init__(self, query: str, params: Tuple[Any, ...] = ()):
        """
        Initialize with SQL query and parameters.

        Args:
            query (str): Parameterized SQL query (e.g., "SELECT ... WHERE age > ?")
            params (Tuple): Tuple of parameters to safely pass to execute()
        """
        self.query = query
        self.params = params
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self):
        """
        Open connection, execute query, return cursor for fetching results.

        Returns:
            sqlite3.Cursor: Cursor with executed query results
        """
        try:
            # Open connection
            self.conn = sqlite3.connect("users.db")
            self.conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
            self.cursor = self.conn.cursor()

            # Execute query with parameters
            print(f"Executing query: {self.query}")
            print(f"With parameters: {self.params}")
            self.cursor.execute(self.query, self.params)

            return self.cursor  # This is what 'as cursor' receives

        except sqlite3.Error as e:
            raise RuntimeError(f"Query execution failed: {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commit if successful, rollback on error, always close connection.

        Args:
            exc_type, exc_value, traceback: Exception info (or None)

        Returns:
            bool: False → let exceptions propagate
        """
        if self.conn:
            try:
                if exc_type is None:
                    self.conn.commit()
                    print("Query executed and committed.")
                else:
                    self.conn.rollback()
                    print(f"Query failed → rolled back: {exc_value}")
            except sqlite3.Error as e:
                print(f"Transaction handling error: {e}")
            finally:
                try:
                    self.conn.close()
                    print("Database connection closed.")
                except sqlite3.Error as e:
                    print(f"Error closing connection: {e}")

        return False  # Do not suppress exceptions


# ————————————————————————————————————————————————————————————————
# Demo: Use the context manager with the required query
# ————————————————————————————————————————————————————————————————

def create_sample_db() -> None:
    """Create users table with 'age' column and insert sample data."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Force drop to avoid schema mismatch
    cursor.execute("DROP TABLE IF EXISTS users")
    print("Dropped existing 'users' table to ensure correct schema.")

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER
        )
    """)
    print("Created 'users' table with 'age' column.")

    # Insert users with different ages
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 22),
        ("Charlie", "charlie@example.com", 28),
        ("Diana", "diana@example.com", 19),
    ]
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        users
    )
    conn.commit()
    conn.close()
    print("Inserted sample users with ages.")


def main() -> None:
    """Demo using ExecuteQuery with the required query."""
    # Ensure DB exists
    create_sample_db()

    print("\n" + "="*60)
    print("EXECUTING: SELECT * FROM users WHERE age > ? (param: 25)")
    print("="*60)

    # Use the reusable context manager
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    try:
        with ExecuteQuery(query, param) as cursor:
            results: List[sqlite3.Row] = cursor.fetchall()

            if results:
                print(f"\nFound {len(results)} user(s) older than 25:\n")
                for row in results:
                    print(f"  ID: {row['id']}")
                    print(f"  Name: {row['name']}")
                    print(f"  Email: {row['email']}")
                    print(f"  Age: {row['age']}")
                    print("  " + "-"*30)
            else:
                print("No users older than 25.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
