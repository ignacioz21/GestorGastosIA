from flask import Blueprint, render_template, request, redirect, url_for
from src.database.helpeDB import add_expense, get_expenses, add_expenses_PLM
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            name = request.form['expense-name']
            amount = float(request.form['expense-value'])
            date = datetime.strptime(request.form['expense-date'], '%Y-%m-%d').date()
            category = request.form['expense-category']
            if add_expense(name, amount, date, category):
                print('Expense added successfully.')
            else:
                print('Failed to add expense.')
        except ValueError as e:
            print(f'ValueError: {str(e)}')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            
        return redirect(url_for('main.home'))
    expenses = get_expenses()
    return render_template('home.html', expenses=expenses)


@bp.route('/PLM', methods=['GET', 'POST'])
def plm():
    text = request.form.get('expense_text', '')
    amount = float(request.form.get('expense_value', None))
    success, message = add_expenses_PLM(text, amount)
    if success:
        print('PLM expenses processed successfully.')
    else:
        print(f'Error processing PLM expenses: {message}')
    return render_template('prueba2.html')