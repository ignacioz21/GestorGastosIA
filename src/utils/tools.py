from src.database.helpeDB import *

def getHomeValues():
    values = []
    recentExpenses = getRecentExpense()
    typeTransaction = getEnums('MOVEMENT')
    category, amount = getExpenseCategory()
    categories = getCategories()
    values.append(recentExpenses)
    values.append(typeTransaction)
    values.append(category)
    values.append(amount)
    values.append(categories)
    return values

