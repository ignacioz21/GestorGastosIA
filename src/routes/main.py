from flask import Blueprint, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from src.IA.utils.image_processing import extract_text, extract_text_pdf

from src.database.helpeDB import add_expense, get_expenses, add_expenses_PLM, get_expenses_PLM
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if 'ticket_image' not in request.files:
            print('No file uploaded', 'error')
            return redirect(url_for('main.ocr'))
        
        file = request.files['ticket_image']
        
        if file.filename == '':
            print('No file selected', 'error')
            return redirect(url_for('main.ocr'))
            
        try:
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            
            # Save file temporarily
            temp_path = os.path.join('temp', secure_filename(file.filename))
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)
            
            try:
                if file_ext == 'pdf':
                    text = extract_text_pdf(temp_path)
                else:
                    text = extract_text(temp_path)
                    
                if text:
                    print(f'Extracted text: {text}', 'success')
                else:
                    print('No text could be extracted', 'warning')
                    
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            print(f'Error processing file: {str(e)}', 'error')
            
        return redirect(url_for('main.ocr'))
        
    return render_template('prueba3.html')