#!/usr/bin/env python3
"""
3-concurrent.py

Demonstrates **concurrent async database queries** using:
- `aiosqlite` (async SQLite)
- `asyncio.gather()` to run queries in parallel
- Two async functions: fetch all users + fetch users > 40

"""

import asyncio
import aiosqlite
from typing import List, Dict


# ————————————————————————————————————————————————————————————————
# Sample DB setup (with users aged 10–50)
# ————————————————————————————————————————————————————————————————

async def create_sample_db() -> None:
    """Create users table and insert sample data with ages 10–50."""
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            DROP TABLE IF EXISTS users
        """)
        await db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                age INTEGER
            )
        """)

        users = [
            (f"User{i}", f"user{i}@example.com", 10 + (i * 5) % 41)
            for i in range(1, 11)
        ]  # ages: 15, 20, 25, ..., 50

        await db.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            users
        )
        await db.commit()
        print("Sample database created with users aged 15–50.")


# ————————————————————————————————————————————————————————————————
# Async Query Functions
# ————————————————————————————————————————————————————————————————

async def async_fetch_users() -> List[Dict]:
    """
    Fetch ALL users from the database asynchronously.

    Returns:
        List of user dicts: [{'id': 1, 'name': '...', 'email': '...', 'age': 25}, ...]
    """
    print("Starting: Fetch ALL users...")
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            users = [dict(row) for row in rows]
            print(f"Completed: Fetched {len(users)} users.")
            return users


async def async_fetch_older_users() -> List[Dict]:
    """
    Fetch users older than 40 asynchronously.

    Returns:
        List of user dicts where age > 40
    """
    print("Starting: Fetch users older than 40...")
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            older_users = [dict(row) for row in rows]
            print(f"Completed: Fetched {len(older_users)} users older than 40.")
            return older_users


# ————————————————————————————————————————————————————————————————
# Concurrent Execution
# ————————————————————————————————————————————————————————————————

async def fetch_concurrently() -> None:
    """Run both queries concurrently using asyncio.gather()."""
    print("\n" + "="*60)
    print("RUNNING QUERIES CONCURRENTLY")
    print("="*60)

    # Run both async functions at the same time
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    # Print results
    print("\n" + "—"*50)
    print("FINAL RESULTS")
    print("—"*50)
    print(f"All users ({len(all_users)}):")
    for u in all_users:
        print(f"  • {u['name']} ({u['age']} y/o)")

    print(f"\nUsers older than 40 ({len(older_users)}):")
    for u in older_users:
        print(f"  • {u['name']} ({u['age']} y/o)")


# ————————————————————————————————————————————————————————————————
# Main Entry Point
# ————————————————————————————————————————————————————————————————

async def main() -> None:
    """Setup DB and run concurrent queries."""
    await create_sample_db()
    await fetch_concurrently()


# Run with asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())
