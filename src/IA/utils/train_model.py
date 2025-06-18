import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from joblib import dump
import os
from pathlib import Path

# Set up paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = os.path.join(BASE_DIR, 'dataset', 'text_facturas.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'IA', 'models', 'bills_models.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'IA', 'models', 'bills_vector.pkl')

# Load and prepare data
datos = pd.read_csv(DATA_PATH)
datos['date'] = pd.to_datetime(datos['date'], errors='coerce')
datos['date'] = datos['date'].dt.month.fillna(-1)

# Create vectorizer and transform text
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(datos['texto_extraido'])

# Create the preprocessing pipeline for structured data
structured_preprocessor = ColumnTransformer(
    transformers=[
        ('numeric', StandardScaler(), ['amount']),
        ('categorical', OneHotEncoder(sparse_output=False), ['date'])
    ]
)

# Create and fit the model
model = LogisticRegression()
model.fit(X_text, datos['categoria'])

# Save both the model and vectorizer
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
dump(model, MODEL_PATH)
dump(vectorizer, VECTOR_PATH)

print('Model and vectorizer saved successfully.')