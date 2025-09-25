from src.database.helpeDB import get5RecentExpenses, getEnums, getTopCategories, getCategories
from src.IA.utils.tools import extrac_category

def getHomeValues():
    values = []
    recentExpenses = get5RecentExpenses()
    typeTransaction = getEnums('MOVEMENT')
    topCategories, amount = getTopCategories() 
    categories = getCategories()
    values.append(recentExpenses)
    values.append(typeTransaction)
    values.append(categories)
    values.append(topCategories)
    values.append(amount)
    return values


def PLM_expenses_loading(text, amount):
    category = extrac_category(text)

    return {
        'category': category,
        'text': text,
        'amount': amount
    }

