from . import get_db_connection
from datetime import datetime
from mysql.connector import Error
from src.IA.utils.tools import extrac_category, extract_bills_atributes, change_date_format
from src.utils.tools import *

def add_expense(category, type, movement, name, amount, date):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("addExpense", [category, type, movement, name, amount, date])
            connection.commit()
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
            cursor.callproc("getExpenses")
            expenses = cursor.fetchall()
            cursor.close()
            connection.close()
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

def getEnums(columName):
    connection = get_db_connection()
    enums = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getEnums", [columName])

            for result in cursor.stored_results():
                values = result.fetchall()
                dirtyEnums = [column[list(column.keys())[0]] for column in values]
            
            dirtyEnums = dirtyEnums[0]
            cleanEnums = dirtyEnums.replace("enum(","").replace(")", "")

            enums = cleanEnums.split(",")
            enums = [e.strip().strip("'") for e in enums]

            return enums
        except Error as e:
            print(f"Error en la funcion getEnums(): \n{e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")


def addCategory(name):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("addCategory", [name])

            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    idCategory = row[0]

            print(f"Categoria agregada: {name} con ID {idCategory}")
            connection.commit()
            return idCategory

        except Error as e:
            print(f"Error en la funcion 'addCategory' => {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
                print("MySQL disconnected")

def getCategories():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("GetCategoryNames")
            for result in cursor.stored_results():
                categories = result.fetchall()
            return categories
        except Error as e:
            print(f"Error en la funcion 'getCategories' => {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")


def get5RecentExpenses():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("get5Expenses")
            for result in cursor.stored_results():
                expenses = result.fetchall()
            return expenses
        except Error as e:
            print(f"Error en la funcion 'get5RecentExpenses' => {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")



def getTopCategories():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("getTopCategories")
            for result in cursor.stored_results():
                results = result.fetchall()
            categories = [row[0] for row in results]
            amounts = [row[1] for row in results]
            return categories, amounts
        except Exception as e:
            print(f"Error obteniendo los gastos recientes: {e}")
            return [], []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Conexion categoria cerrada")


def getTotalByMovement(movement_type):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # importante
            cursor.callproc("getTotalByMovement", [movement_type])

            result_dict = {"movement": movement_type, "total": 0}
            for result in cursor.stored_results():
                rows = result.fetchall()
                if rows and "TOTAL_AMOUNT" in rows[0]:
                    result_dict["total"] = rows[0]["TOTAL_AMOUNT"] or 0

            return result_dict

        except Exception as e:
            print(f"Error en getTotalByMovement: {e}")
            return {"movement": movement_type, "total": 0}
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
