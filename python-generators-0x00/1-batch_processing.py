#!/usr/bin/env python3
"""
Batch processing with filtering module.
Processes users in batches and filters based on age criteria.
"""
import os
import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
        
    Yields:
        list: A list of dictionaries, each representing a user row
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
        
        # Fetch and yield batches (loop 1)
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except Error as e:
        print(f"Error streaming users in batches: {e}")
    finally:
        # Cleanup resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users and filters those over age 25.
    Uses a maximum of 3 loops total.
    
    Args:
        batch_size (int): Number of rows to process per batch
    """
    # Loop 2: Iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Process each user in the batch
        for user in batch:
            if user['age'] > 25:
                print(user)
