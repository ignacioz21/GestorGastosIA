from src.database.helpeDB import add_expense, add_expenses_PLM

def addManualExpense(value):
    if value != None:
        amount = value.get('expense-value')
        name = value.get('expense-name')
        date = value.get('expense-date')
        category = value.get('expense-category')
        return add_expense(name, amount, date, category)
    return False


def addIAExpense(value):
    if value != None:
        text = value.get('ia-description')
        amount = value.get('ia-amount')
        date = value.get('ia-date')
        return add_expenses_PLM(text, amount, date)
    return False