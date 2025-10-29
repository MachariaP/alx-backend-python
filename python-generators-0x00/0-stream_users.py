#!/usr/bin/env python3
"""
Row-by-row streaming generator module.
Streams user data from MySQL one record at a time using yield.
"""
import os
import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: A dictionary containing user_id, name, email, and age for each row
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
        cursor.execute("SELECT * FROM user_data")
        
        # Yield rows one at a time (single loop)
        for row in cursor:
            yield row
            
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        # Cleanup resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
