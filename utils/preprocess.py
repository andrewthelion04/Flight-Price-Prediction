import pandas as pd


def preprocess_data(data):
    # Curățare și conversie
    data['Date_of_Journey'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y')
    data['Dep_Time'] = pd.to_datetime(data['Dep_Time'], format='%H:%M').dt.time

    # Transformă Date_of_Journey în numărul de zile de la o dată de referință
    data['Journey_day'] = data['Date_of_Journey'].dt.day
    data['Journey_month'] = data['Date_of_Journey'].dt.month
    data['Journey_year'] = data['Date_of_Journey'].dt.year

    # Extrage ore și minute din Dep_Time
    data['Dep_Hour'] = data['Dep_Time'].apply(lambda x: x.hour)
    data['Dep_Minute'] = data['Dep_Time'].apply(lambda x: x.minute)

    # Modifică prelucrarea duratei pentru a accepta ambele formate
    data['Duration_hours'] = data['Duration'].str.extract(r'(\d+)h').fillna(0).astype(int)
    data['Duration_minutes'] = data['Duration'].str.extract(r'(\d+)m').fillna(0).astype(int)

    # Înlocuiește NaN cu 0 pentru minute acolo unde este necesar
    data['Duration_minutes'] = data['Duration_minutes'].fillna(0).astype(int)

    # Calculăm durata totală în minute
    data['Duration_total_minutes'] = data['Duration_hours'] * 60 + data['Duration_minutes']

    # Gestionăm valorile lipsă pentru 'Route' și aplicăm preprocesarea
    data['Route'] = data['Route'].fillna('')  # Înlocuim valorile NaN cu un șir gol
    data['Route'] = data['Route'].apply(lambda x: ' → '.join(sorted(str(x).split(' → '))) if isinstance(x, str) else '')

    # Elimina coloana nesemnificativă (de exemplu 'Additional_Info') care conține valori de tipul 'No info'
    data = data.drop(columns=['Additional_Info'],
                     errors='ignore')  # înlocuiește 'Additional_Info' cu numele real al coloanei

    # Codificare categorică
    data = pd.get_dummies(data, columns=['Airline', 'Source', 'Destination', 'Total_Stops', 'Route'], drop_first=True)

    # Selectează X și y
    X = data.drop(['Price', 'Duration', 'Arrival_Time', 'Date_of_Journey', 'Dep_Time'], axis=1)
    y = data['Price']

    return X, y

def preprocess_input(input_data):
    # Funcție pentru preprocesarea input-ului utilizatorului
    df = pd.DataFrame([input_data])
    df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], format='%Y-%m-%d')
    df['Duration_total_minutes'] = df['Duration_hours'] * 60 + df['Duration_minutes']
    df = df.drop(['Duration_hours', 'Duration_minutes'], axis=1)
    return df.iloc[0].values
