from src.database.helpeDB import getTotalByMovement, getTopCategories, get5RecentExpenses, getCategories, getEnums
from src.IA.utils.tools import extrac_category


def getHomeValues(user_id):
    totalExpenses = getTotalByMovement(user_id, 'expense')
    totalIncome = getTotalByMovement(user_id, 'income')
    totalSavings = getTotalByMovement(user_id, 'savings')
    mostCategories, mostAmounts = getTopCategories(user_id)
    recent5expenses = get5RecentExpenses(user_id)
    categories = getCategories(user_id)
    enumsType = getEnums('MOVEMENT')
    return {
        'totalExpenses': totalExpenses,
        'totalIncome': totalIncome,
        'totalSavings': totalSavings,
        'mostCategories': mostCategories,
        'mostAmounts': mostAmounts,
        'recentExpenses': recent5expenses,
        'categories': categories,
        'enumsType': enumsType
    }


def PLM_expenses_loading(text, amount):
    category = extrac_category(text)

    return {
        'category': category,
        'text': text,
        'amount': amount
    }
