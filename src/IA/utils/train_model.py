import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from joblib import dump
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = os.path.join(BASE_DIR, 'dataset', 'datos.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'IA', 'models', 'spending_models.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'IA', 'models', 'spending_vector.pkl')

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Data file not found at: {DATA_PATH}")

datos = pd.read_csv(DATA_PATH)

texts = datos['descripcion']
categories = datos['categoria']

vector = TfidfVectorizer()
X = vector.fit_transform(texts)

model = LogisticRegression()
model.fit(X, categories)

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

dump(model, MODEL_PATH)
dump(vector, VECTOR_PATH)

print('Model and vectorizer saved successfully.')