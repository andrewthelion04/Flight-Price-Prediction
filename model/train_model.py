import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import sys
import os

# Adaugă directorul rădăcină al proiectului în sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Încarcă dataset-ul
data = pd.read_excel('data/dataset.xlsx')

# Preprocesează datele (detalii în `preprocess.py`)
from utils.preprocess import preprocess_data
X, y = preprocess_data(data)

# Împarte în seturi de antrenament și test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Antrenează modelul
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salvează modelul
joblib.dump(model, 'model/flight_price_model.pkl')
print("Model salvat cu succes!")
