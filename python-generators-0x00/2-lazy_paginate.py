#!/usr/bin/env python3
"""
Lazy pagination module.
Implements on-demand page loading using LIMIT and OFFSET.
"""
import os
import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the database.
    
    Args:
        page_size (int): Number of rows per page
        offset (int): Starting position for the query
        
    Returns:
        list: List of user dictionaries for the requested page
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        
        rows = cursor.fetchall()
        return rows
            
    except Error as e:
        print(f"Error paginating users: {e}")
        return []
    finally:
        # Cleanup resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
    Generator function that lazily loads pages of users on demand.
    Uses one loop for pagination logic.
    
    Args:
        page_size (int): Number of rows per page
        
    Yields:
        list: A page (list) of user dictionaries
    """
    offset = 0
    
    # Single loop for pagination
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
