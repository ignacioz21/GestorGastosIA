from src.database.helpeDB import *

def getHomeValues():
    values = []
    recentExpenses = getRecentExpense()
    typeTransaction = getEnums('MOVEMENT')
    category, amount = getExpenseCategory() 
    values.append(recentExpenses)
    values.append(typeTransaction)
    values.append(category)
    values.append(amount)
    return values

