from joblib import load
import os
from pathlib import Path
import re
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_model():
    model_path = os.path.join(BASE_DIR, 'IA', 'models', 'spending_models.pkl')
    vector_path = os.path.join(BASE_DIR, 'IA', 'models', 'spending_vector.pkl')

    model = load(model_path)
    vectorizer = load(vector_path)
    return model, vectorizer


def extrac_category(text):
    try:
        model, vectorizer = load_model()
        X = vectorizer.transform([text])
        category = model.predict(X)[0]
        return category
    except Exception as e:
        print(f"Error extracting category: {e}")
        return "Others"


def load_bills_model():
    model_path = os.path.join(BASE_DIR, 'IA', 'models', 'bills_models.pkl')
    vector_path = os.path.join(BASE_DIR, 'IA', 'models', 'bills_vector.pkl')
    model = load(model_path)
    vectorizer = load(vector_path)
    return model, vectorizer


def extract_bills_atributes(text):
    try:
        model, vectorizer = load_bills_model()
        X = vectorizer.transform([text])
        category = model.predict(X)[0]
        
        amount_pattern = r'\₡?\d+\.?\d*'
        amounts = re.findall(amount_pattern, text)
        amount = float(amounts[0].replace('₡', '').replace('.', '').replace(',', '.')) if amounts else 0.0

        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        dates = re.findall(date_pattern, text)
        date = dates[0] if dates else None
        date = change_date_format(date)
        
        name_patterns = [
            r'(?i)empresa:?\s*([A-Za-z0-9\s&]+?)(?=\s*(?:S\.A\.|LTDA\.?|INC\.?|$))',
            r'(?i)negocio:?\s*([A-Za-z0-9\s&]+)',
            r'(?i)tienda:?\s*([A-Za-z0-9\s&]+)',
            r'(?i)factura\s+de:?\s*([A-Za-z0-9\s&]+)'
        ]
        
        name = None
        for pattern in name_patterns:
            matches = re.search(pattern, text)
            if matches:
                name = matches.group(1).strip()
                break
                
        if not name and text:
            first_line = text.split('\n')[0].strip()
            name = first_line if first_line else "Unknown Vendor"

        return {
            'category' : category,
            'amount' : amount,
            'date' : date
        }
    except Exception as e:
        print(f"Error extracting bill attributes: {e}")
        return {
            'category': "Others",
            'amount': 0.0,
            'date': None,
            'name': "Unknown Vendor"
        }
    

def change_date_format(date_str):
    try:
        if date_str:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        return None
    except ValueError:
        return None
    except Exception as e:
        print(f"Error changing date format: {e}")
        return None