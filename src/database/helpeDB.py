from . import get_db_connection
from datetime import datetime
from mysql.connector import Error
 
def add_expense(name, amount, date, category):
    now = datetime.now();
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO expenses (NAME, AMOUNT, DATE, CATEGORY, CREATED_AT)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, amount, date, category, now))
            connection.commit()
            print("Expense added successfully.")
            return True
        except Error as e:
            print(f"Error while adding expense: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

def get_expenses():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM expenses"
            cursor.execute(query)
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print(f"Error while fetching expenses: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")
    return []