import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='gestorIA',
            user = 'root',
            password = '07-04-07'
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
                            CREATE TABLE IF NOT EXISTS expenses (
                                    ID INT AUTO_INCREMENT PRIMARY KEY,
                                    NAME VARCHAR(100) NOT NULL,
                                    AMOUNT DECIMAL NOT NULL,
                                    DATE DATE NOT NULL,
                                    CATEGORY VARCHAR(50),
                                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                            """)
            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS expensesPLN (
	                                ID INT AUTO_INCREMENT PRIMARY KEY,
                                    CATEGORIA VARCHAR(100) NOT NULL,
                                    AMOUNT DECIMAL NOT NULL,
                                    DATE DATE NOT NULL,
                                    PROMPT VARCHAR(255) NOT NULL
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
                print("MySQL connection is closed.")