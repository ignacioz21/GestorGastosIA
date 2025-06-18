from joblib import load
import os
from pathlib import Path
import re

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
            'date': None
        }