from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify, session
from functools import wraps
from src.IA.utils.image_processing import extract_text, extract_text_pdf
from src.utils.tools import getHomeValues
from src.database.helpeDB import add_expense, addCategory, getTopCategories, delete_expense
from src.IA.utils.tools import extrac_category
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_id = session['user_id']

    if request.method == 'POST':
        value = request.form.get('form_type')

        if value == "ia":
            description = request.form.get('ia-description', '')
            amount = request.form.get('ia-amount')
            date = request.form.get('ia-date')

            if description and amount and date:
                category_name = extrac_category(description)
                category_id = addCategory(user_id, category_name)
                if category_id:
                    add_expense(
                        user_id=user_id,
                        category=category_id,
                        type='plm',
                        movement='Expense',
                        name=description,
                        amount=amount,
                        date=date
                    )

        elif value == "manual":
            boxValues = request.form
            name = boxValues.get('expense-name')
            amount = boxValues.get('expense-value')
            date = boxValues.get('expense-date')
            selected_category = boxValues.get('expense-category')
            transaction = boxValues.get('transaction')

            if selected_category != "new-category":
                add_expense(
                    user_id=user_id,
                    category=selected_category,
                    type='manual',
                    movement=transaction,
                    name=name,
                    amount=amount,
                    date=date
                )
            else:
                newCategory = boxValues.get('expense-category-new')
                cat_id = addCategory(user_id, newCategory)
                add_expense(
                    user_id=user_id,
                    category=cat_id,
                    type='manual',
                    movement=transaction,
                    name=name,
                    amount=amount,
                    date=date
                )

        return redirect(url_for('main.home'))

    valuesHome = getHomeValues(user_id)
    chart_data = None
    try:
        if isinstance(valuesHome['mostCategories'], list) and isinstance(valuesHome['mostAmounts'], list):
            gastos_combinados = list(zip(valuesHome['mostCategories'], valuesHome['mostAmounts']))
            gastos_ordenados = sorted(gastos_combinados, key=lambda x: x[1], reverse=True)

            chart_data = {
                'categorias': [item[0] for item in gastos_ordenados],
                'montos': [float(item[1]) for item in gastos_ordenados]
            }
    except:
        chart_data = None

    return render_template('home.html', value=valuesHome, chart_data=chart_data)


@bp.route('/lista-gastos', methods=['GET', 'POST'])
@login_required
def listaGastos():
    user_id = session['user_id']
    valuesHome = getHomeValues(user_id)
    return render_template('expense.html', value=valuesHome)


@bp.route('/api/gastos-categoria', methods=['GET'])
@login_required
def obtenerExpenseCategory():
    user_id = session['user_id']
    try:
        category, amount = getTopCategories(user_id)

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


@bp.route('/api/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def deleteExpense(expense_id):
    user_id = session['user_id']
    result = delete_expense(expense_id, user_id)
    if result:
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'error': 'No se pudo eliminar'}), 400
