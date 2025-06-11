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
