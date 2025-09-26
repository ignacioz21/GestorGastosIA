from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from src.IA.utils.image_processing import extract_text, extract_text_pdf
from src.utils.tools import getHomeValues
from src.database.helpeDB import *
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        value = request.form.get('form_type')
        boxValues = request.form
        print(value)
        if value == "ia":
            print("Seleccionaste IA")
    
        elif value == "manual":
            name = boxValues.get('expense-name')
            amount = boxValues.get('expense-value')
            date = boxValues.get('expense-date')
            selected_category = boxValues.get('expense-category')
            transaction = boxValues.get('transaction')
            print(selected_category)
            categoryId = 0
            

            if selected_category != "new-category":
                check = add_expense(
                    category=selected_category, 
                    type='manual', 
                    movement=transaction, 
                    name=name, 
                    amount=amount, 
                    date=date
                    )
                print(f"Gasto '{name}' agregado en categoría ID {categoryId}")
                print(check)
            else:
                newCategory = boxValues.get('expense-category-new')
                id = addCategory(newCategory)
                check = add_expense(
                    category=id, 
                    type='manual', 
                    movement=transaction, 
                    name=name, 
                    amount=amount, 
                    date=date
                )

        return redirect(url_for('main.home'))


    valuesHome = getHomeValues()
    print(valuesHome)
    chart_data = None
    try:
        if isinstance(valuesHome.mostCategories, list) and isinstance(valuesHome.mostCategories, list):
            gastos_combinados = list(zip(valuesHome.mostCategories, amount))
            gastos_ordenados = sorted(gastos_combinados, key=lambda x: x[1], reverse=True)
            
            chart_data = {
                'categorias': [item[0] for item in gastos_ordenados],
                'montos': [float(item[1]) for item in gastos_ordenados]
            }
    except:
        chart_data = None
    

    return render_template('home.html', value=valuesHome, chart_data=chart_data)

@bp.route('/api/gastos-categoria', methods=['GET'])
def obtenerExpenseCategory():
    try:
        category, amount = getTopCategories()

    
        if isinstance(category, list) and isinstance(amount, list):

            unOrderAmount = list(zip(category, amount))
            orderAmount = sorted(unOrderAmount, key=lambda x: x[1], reverse=True)

            categories = [item[0] for item in orderAmount]
            amounts = [float(item[1]) for item in orderAmount]
        else:
            categories = []
            amounts = []

        total = sum(amounts) if amounts else 0.0

        return jsonify({
            'success': True,
            'categorias': categories,
            'montos': amounts,
            'total_gastos': total
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
            
@bp.route('/debug-expense-data')
def debug_expense_data():
    try:
        category, amount = getTopCategories()
        return {
            'category_type': str(type(category)),
            'category_value': category,
            'amount_type': str(type(amount)),
            'amount_value': amount,
            'category_length': len(category) if hasattr(category, '__len__') else 'N/A',
            'amount_length': len(amount) if hasattr(amount, '__len__') else 'N/A'
        }
    except Exception as e:
        return {'error': str(e)}
