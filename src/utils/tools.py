from src.database.helpeDB import getTotalByMovement, getTopCategories, get5RecentExpenses, getCategories, getEnums
from src.IA.utils.tools import extrac_category

def getHomeValues():
    totalExpenses = getTotalByMovement('expense')
    totalIncome = getTotalByMovement('income')
    totalSavings = getTotalByMovement('savings')
    mostCategories, mostAmounts = getTopCategories()
    recent5expenses = get5RecentExpenses()
    categories = getCategories()
    enumsType = getEnums('MOVEMENT')
    return {
        'totalExpenses' : totalExpenses,
        'totalIncome' : totalIncome,
        'totalSavings' : totalSavings,
        'mostCategories' : mostCategories,
        'mostAmounts' : mostAmounts,
        'recentExpenses' : recent5expenses,
        'categories' : categories,
        'enumsType' : enumsType
    }


def PLM_expenses_loading(text, amount):
    category = extrac_category(text)

    return {
        'category': category,
        'text': text,
        'amount': amount
    }

