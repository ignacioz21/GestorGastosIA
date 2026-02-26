import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'gestorIA'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def init_db():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    EMAIL VARCHAR(255) NOT NULL UNIQUE,
                    PASSWORD_HASH VARCHAR(255) NOT NULL,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    USER_ID INT,
                    NAME VARCHAR(100) NOT NULL,
                    FOREIGN KEY (USER_ID) REFERENCES users(ID) ON DELETE CASCADE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    USER_ID INT NOT NULL,
                    CATEGORY INT,
                    TYPE ENUM('plm', 'manual', 'ocr'),
                    MOVEMENT ENUM('Income', 'Expense', 'Savings'),
                    NAME VARCHAR(100) NOT NULL,
                    AMOUNT DECIMAL(10,2) NOT NULL,
                    DATE DATE NOT NULL,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (CATEGORY) REFERENCES categories(ID),
                    FOREIGN KEY (USER_ID) REFERENCES users(ID) ON DELETE CASCADE
                )
            """)
            connection.commit()
            print("Database initialized successfully.")
        except Error as e:
            print(f"Error while initializing the database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
