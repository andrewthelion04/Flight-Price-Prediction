from flask import Flask, request, render_template
import joblib
import pandas as pd
from utils.preprocess import preprocess_input

# Inițializare aplicație Flask
app = Flask(__name__)

# Încarcă modelul antrenat
model = joblib.load('model/flight_price_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Preia datele din formular
        data = {
            'Airline': request.form['airline'],
            'Date_of_Journey': request.form['date_of_journey'],
            'Source': request.form['source'],
            'Destination': request.form['destination'],
            'Total_Stops': request.form['total_stops'],
            'Dep_Time': request.form['dep_time'],
            'Duration_hours': request.form['duration_hours'],
            'Duration_minutes': request.form['duration_minutes']
        }
        
        # Preprocesează datele
        input_data = preprocess_input(data)
        
        # Realizează predicția
        prediction = model.predict([input_data])[0]
        
        return render_template('index.html', prediction=f"Preț estimat: {round(prediction, 2)}")
