import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import sys
import os

def preprocess_data(data):
    # Conversii de date
    data['Date_of_Journey'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y')
    data['Date_of_Journey'] = (data['Date_of_Journey'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1D')

    data['Dep_Time'] = pd.to_datetime(data['Dep_Time'], format='%H:%M')
    data['Dep_Hour'] = data['Dep_Time'].dt.hour
    data['Dep_Minute'] = data['Dep_Time'].dt.minute

    data['Duration_hours'] = data['Duration'].str.extract(r'(\d+)h').fillna(0).astype(int)
    data['Duration_minutes'] = data['Duration'].str.extract(r'(\d+)m').fillna(0).astype(int)
    data['Duration_total_minutes'] = data['Duration_hours'] * 60 + data['Duration_minutes']

    # Drop coloane nefolositoare
    data = data.drop(['Duration', 'Dep_Time', 'Arrival_Time'], axis=1)

    # Codificare categorică
    categorical_columns = ['Airline', 'Source', 'Destination', 'Total_Stops']
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    
    # Selectează X și y
    X = data.drop(['Price'], axis=1)
    y = data['Price']
    return X, y

# Adaugă directorul rădăcină al proiectului în sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Încarcă dataset-ul
data = pd.read_excel('data/dataset.xlsx')

# Preprocesează datele (detalii în `preprocess.py`)
#from utils.preprocess import preprocess_data
X, y = preprocess_data(data)

# Împarte în seturi de antrenament și test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Antrenează modelul
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salvează modelul
joblib.dump(model, 'model/flight_price_model.pkl')
print("Model salvat cu succes!")
