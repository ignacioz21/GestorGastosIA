from . import get_db_connection
from datetime import datetime
from mysql.connector import Error
from src.IA.utils.tools import extrac_category, extract_bills_atributes, change_date_format
 
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
            cursor.execute("""
                SELECT id, name, amount, 
                       DATE_FORMAT(date, '%Y-%m-%d') as date, 
                       category, created_at 
                FROM expenses 
                ORDER BY date DESC
            """)
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print(f"Error fetching expenses: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
    return []

def PLM_expenses_loading(text, amount):
    category = extrac_category(text)
    now = datetime.now()

    return {
        'category': category,
        'now': now,
        'text': text,
        'amount': amount
    }


def add_expenses_PLM(text, amount):
    processessed_data = PLM_expenses_loading(text, amount)
    if processessed_data['amount'] is None:
        return False, "Amount is required"
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO expensesPLN (CATEGORIA, AMOUNT, DATE, PROMPT) VALUES (%s, %s, %s, %s)
                """
            values = (
                processessed_data['category'],
                processessed_data['amount'],
                processessed_data['now'],
                processessed_data['text']
            )
            cursor.execute(query, values)
            connection.commit()
            print("PLM expense added successfully.")
            return True, "Expense added successfully"
        except Error as e:
            print(f"Error while adding PLM expense: {str(e)})")
            return False, f"Error while adding PLM expense: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")
    return False, "Database connection failed"



def atributes_extraction_OCR(text):
    try:
        atributes = extract_bills_atributes(text)
        if atributes['date'] is None:
            atributes['date'] = datetime.now().strftime('%Y-%m-%d')
            atributes['date'] = change_date_format(atributes['date'])
            print(atributes['date'])
        return atributes
    except Exception as e:
        print(f"Error extracting attributes from OCR text: {e}")
        return {
            'category': "Others",
            'amount': 0.0,
            'date': datetime.now().strftime('%Y-%m-%d') # Escape single quotes for SQL
        }
        

def get_expenses_PLM():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, categoria, amount, 
                       DATE_FORMAT(date, '%Y-%m-%d') as date, 
                       prompt 
                FROM expensesPLN 
                ORDER BY date DESC
            """)
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print(f"Error fetching PLM expenses: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
    return []


def add_expenses_OCR(category, amount, date, name):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO expensesOCR (CATEGORIA, AMOUNT, DATE, NOMBRE)
                VALUES (%s, %s, %s, %s)
            """
            values = (category, amount, date, name)
            print(values)
            cursor.execute(query, values)
            connection.commit()
            print("OCR expense added successfully.")
            return True
        except Error as e:
            print(f"Error while adding OCR expense: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")
    return False


def get_expenses_OCR():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, categoria, amount, 
                       DATE_FORMAT(DATE, '%Y-%m-%d') as date, 
                       nombre 
                FROM expensesOCR 
                ORDER BY DATE DESC
            """)
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print(f"Error fetching OCR expenses: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
    return []