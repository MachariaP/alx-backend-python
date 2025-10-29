#!/usr/bin/env python3
"""
Memory-efficient aggregation module.
Computes average age without loading the entire dataset into memory.
"""
import os
import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator function that yields user ages one at a time.
    
    Yields:
        float: Age of each user from the database
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
        
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Loop 1: Yield ages one at a time
        for (age,) in cursor:
            yield age
            
    except Error as e:
        print(f"Error streaming user ages: {e}")
    finally:
        # Cleanup resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Calculates the average age of users using incremental computation.
    Uses a maximum of 2 loops (one in stream_user_ages, one here).
    
    Returns:
        float: Average age of all users, or None if no users exist
    """
    total_age = 0
    count = 0
    
    # Loop 2: Compute average incrementally
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return None
    
    return total_age / count
