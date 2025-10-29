#!/usr/bin/env python3
"""
Database initialization and seeding module.
Creates ALX_prodev database and user_data table, then seeds with CSV data.
"""
import csv
import os
import mysql.connector
from mysql.connector import Error


def connect_to_prodev():
    """
    Connects to the ALX_prodev MySQL database.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_database(connection):
    """
    Creates the ALX_prodev database if it doesn't exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_db():
    """
    Connects to MySQL server (without specifying a database).
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_table(connection):
    """
    Creates the user_data table with proper schema and indexing.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into user_data table.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
        csv_file: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        email = VALUES(email),
                        age = VALUES(age)
                    """,
                    (row['user_id'], row['name'], row['email'], float(row['age']))
                )
        
        connection.commit()
        cursor.close()
        print(f"Data from {csv_file} inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"Error: CSV file {csv_file} not found")


if __name__ == "__main__":
    # Connect to MySQL server and create database
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
    
    # Connect to ALX_prodev database and set up table
    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(script_dir, 'user_data.csv')
        
        insert_data(conn, csv_file_path)
        conn.close()
