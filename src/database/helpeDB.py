from . import get_db_connection
from datetime import datetime
from mysql.connector import Error

# ============================================
# USER FUNCTIONS
# ============================================

def create_user(name, email, password_hash):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("createUser", [name, email, password_hash])
            for result in cursor.stored_results():
                user = result.fetchone()
            connection.commit()
            return user
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def get_user_by_email(email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getUserByEmail", [email])
            for result in cursor.stored_results():
                user = result.fetchone()
            return user
        except Error as e:
            print(f"Error getting user by email: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def get_user_by_id(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getUserById", [user_id])
            for result in cursor.stored_results():
                user = result.fetchone()
            return user
        except Error as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


# ============================================
# EXPENSE FUNCTIONS (user-scoped)
# ============================================

def add_expense(user_id, category, type, movement, name, amount, date):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("addExpense", [user_id, category, type, movement, name, amount, date])
            connection.commit()
            return True
        except Error as e:
            print(f"Error while adding expense: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def get_expenses(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getExpenses", [user_id])
            for result in cursor.stored_results():
                expenses = result.fetchall()
            return expenses
        except Error as e:
            print(f"Error fetching expenses: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return []


def delete_expense(expense_id, user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("deleteExpense", [expense_id, user_id])
            connection.commit()
            return True
        except Error as e:
            print(f"Error deleting expense: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


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


# ============================================
# CATEGORY FUNCTIONS (user-scoped)
# ============================================

def addCategory(user_id, name):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("addCategory", [user_id, name])

            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    idCategory = row[0]

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


def getCategories(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("GetCategoryNames", [user_id])
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


# ============================================
# DASHBOARD FUNCTIONS (user-scoped)
# ============================================

def get5RecentExpenses(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("get5Expenses", [user_id])
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


def getTopCategories(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc("getTopCategories", [user_id])
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


def getTotalByMovement(user_id, movement_type):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getTotalByMovement", [user_id, movement_type])

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


# ============================================
# FILTER FUNCTIONS (user-scoped)
# ============================================

def getExpensesByTypeProcedure(user_id, type):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getExpensesByTypeOPM", [user_id, type])
            for result in cursor.stored_results():
                results = result.fetchall()
            return results
        except Exception as e:
            print(f"Error en getExpensesByTypeProcedure: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def getExpensesByCategory(user_id, idCategory):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getExpensesByCategory", [user_id, idCategory])
            for result in cursor.stored_results():
                results = result.fetchall()
            return results
        except Exception as e:
            print(f"Error en getExpensesByCategory: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def getExpensesByMonthRange(user_id, startMonth, endMonth):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getExpensesByMonthRange", [user_id, startMonth, endMonth])
            for result in cursor.stored_results():
                results = result.fetchall()
            return results
        except Exception as e:
            print(f"Error en getExpensesByMonthRange: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


def getExpensesByAmountRange(user_id, amountMin, amountMax):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc("getExpensesByAmountRange", [user_id, amountMin, amountMax])
            for result in cursor.stored_results():
                results = result.fetchall()
            return results
        except Exception as e:
            print(f"Error en getExpensesByAmountRange: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
