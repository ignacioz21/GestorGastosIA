from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from src.IA.utils.image_processing import extract_text, extract_text_pdf
from src.utils.tools import getHomeValues
from src.database.helpeDB import add_expenses_PLM, get_expenses_PLM, add_expenses_OCR, get_expenses_OCR, atributes_extraction_OCR, add_expense, getRecentExpense, getExpenseCategory
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def home():
    valuesHome = getHomeValues()

    if request.method == 'POST':
        value = request.form.get('form_type')
        boxValues = request.form
        print(value)
        if value == "ia":
            amount = boxValues.get('ia-amount')
            description = boxValues.get('ia-description')
            date = boxValues.get('ia-date')
            
            check, message = add_expenses_PLM(text=description, amount=amount, date=date)

            if check:
                print(message)
    
        elif value == "manual":
            name = boxValues.get('expense-name')
            amount = boxValues.get('expense-value')
            date = boxValues.get('expense-date')
            category = boxValues.get('expense-category')
            transaction = boxValues.get('transaction')

            check = add_expense(name=name, amount=amount, date=date, category=category, movement=transaction, type='manual' )

            if check:
                print("Agregado con exito!")

        return redirect(url_for('main.home'))

    expenses = valuesHome[0]
    transaction = valuesHome[1]
    category = valuesHome[2]
    amount = valuesHome[3]
    categories = valuesHome[4]

    chart_data = None
    try:
        if isinstance(category, list) and isinstance(amount, list):
            gastos_combinados = list(zip(category, amount))
            gastos_ordenados = sorted(gastos_combinados, key=lambda x: x[1], reverse=True)
            
            chart_data = {
                'categorias': [item[0] for item in gastos_ordenados],
                'montos': [float(item[1]) for item in gastos_ordenados]
            }
    except:
        chart_data = None

    return render_template('home.html', value=expenses, chart_data=chart_data, transaction=transaction, categories=categories)

@bp.route('/api/gastos-categoria', methods=['GET'])
def obtenerExpenseCategory():
    try:
        category, amount = getExpenseCategory()

        # Validar correctamente los tipos
        if isinstance(category, list) and isinstance(amount, list):
            # Combinar y ordenar por monto (índice 1)
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
        category, amount = getExpenseCategory()
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


@bp.route('/PLM', methods=['GET', 'POST'])
def plm():
    if request.method == 'POST':
        try:
            # Get form data with validation
            expense_value = request.form.get('expense_value')
            if not expense_value:
                raise ValueError("Expense value is required")
                
            amount = float(expense_value)
            text = request.form.get('prompt_text', '')
            
            success, message = add_expenses_PLM(text, amount)
            if success:
                flash('PLM expenses processed successfully.', 'success')
            else:
                flash(f'Error processing PLM expenses: {message}', 'error')
                
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
        except Exception as e:
            flash(f'Unexpected error: {str(e)}', 'error')
            
        return redirect(url_for('main.plm'))
    
    expenses = get_expenses_PLM()    
    return render_template('prueba2.html', expenses=expenses)


@bp.route('/OCR', methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "ticket_image":
            if 'ticket_image' not in request.files:
                print('No file uploaded', 'error')
                return redirect(url_for('main.ocr'))
            
            file = request.files['ticket_image']
            
            if file.filename == '':
                print('No file selected', 'error')
                return redirect(url_for('main.ocr'))
                
            try:
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                
                # Process file directly without saving
                if file_ext == 'pdf':
                    text = extract_text_pdf(file)
                else:
                    text = extract_text(file)
                    
                if text:
                    print('Text extracted successfully:')
                    atributes = atributes_extraction_OCR(text)


                else:
                    print('No text could be extracted', 'warning')
                    
            except Exception as e:
                print(f'Error processing file: {str(e)}', 'error')
                

            text = get_expenses_OCR()
            return render_template('prueba3.html', expenses=atributes, text=text)
        elif action == "save-db":
            name = request.form['ocr-name']
            amount = float(request.form.get('ocr-amount'))
            date = datetime.strptime(request.form['ocr-date'], '%Y-%m-%d').date()
            category = request.form['ocr-category']
            add_expenses_OCR(category, amount, date, name)
            
    text = get_expenses_OCR()
    return render_template('prueba3.html', expenses={}, text=text)  