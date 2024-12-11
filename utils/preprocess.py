import pandas as pd

def preprocess_data(data):
    # Curățare și conversie
    data['Date_of_Journey'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y')
    data['Dep_Time'] = pd.to_datetime(data['Dep_Time']).dt.time
    data['Duration_hours'] = data['Duration'].str.extract(r'(\d+)h').fillna(0).astype(int)
    data['Duration_minutes'] = data['Duration'].str.extract(r'(\d+)m').fillna(0).astype(int)
    data['Duration_total_minutes'] = data['Duration_hours'] * 60 + data['Duration_minutes']

    # Codificare categorică
    data = pd.get_dummies(data, columns=['Airline', 'Source', 'Destination', 'Total_Stops'], drop_first=True)
    
    # Selectează X și y
    X = data.drop(['Price', 'Duration', 'Arrival_Time'], axis=1)
    y = data['Price']
    return X, y

def preprocess_input(input_data):
    # Funcție pentru preprocesarea input-ului utilizatorului
    df = pd.DataFrame([input_data])
    df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], format='%Y-%m-%d')
    df['Duration_total_minutes'] = df['Duration_hours'] * 60 + df['Duration_minutes']
    df = df.drop(['Duration_hours', 'Duration_minutes'], axis=1)
    return df.iloc[0].values
