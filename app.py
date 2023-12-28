
import pickle
import warnings
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import OneHotEncoder

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/prever', methods=['POST'])
def prever():
    
    arq = open('data/modelo_atraso_voo.pkl','rb')
    modelo = pickle.load(arq)
    arq.close()
    
    data = request.get_json()
    
    # Criando um DataFrame com base nos dados
    columns = [
        'Year',
        'Month',
        'Flight_Number_Marketing_Airline',
        'Cancelled',
        'Diverted',
        'CRSDepTime',
        'DepTime',
        'OriginAirportID',
        'DestAirportID',
        'TaxiOut',
        'TaxiIn',
        'CRSArrTime',
        'ArrTime',
        'ArrDelayMinutes',
        'Airline_Alaska Airlines Inc.',
        'Airline_Allegiant Air',
        'Airline_American Airlines Inc.',
        'Airline_Cape Air',
        'Airline_Capital Cargo International',
        'Airline_Comair Inc.',
        'Airline_Commutair Aka Champlain Enterprises, Inc.',
        'Airline_Compass Airlines',
        'Airline_Delta Air Lines Inc.',
        'Airline_Empire Airlines Inc.',
        'Airline_Endeavor Air Inc.',
        'Airline_Envoy Air',
        'Airline_ExpressJet Airlines Inc.',
        'Airline_Frontier Airlines Inc.',
        'Airline_GoJet Airlines, LLC d/b/a United Express',
        'Airline_Hawaiian Airlines Inc.',
        'Airline_Horizon Air',
        'Airline_JetBlue Airways',
        'Airline_Mesa Airlines Inc.',
        'Airline_Peninsula Airways Inc.',
        'Airline_Republic Airlines',
        'Airline_SkyWest Airlines Inc.',
        'Airline_Southwest Airlines Co.',
        'Airline_Spirit Air Lines',
        'Airline_Trans States Airlines',
        'Airline_United Air Lines Inc.',
        'Airline_Virgin America']

    df = pd.DataFrame([data], columns=columns)

    print(data)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Aplicar OneHotEncoder nas variaveis categoricas
    ohe = OneHotEncoder(handle_unknown='ignore', drop='first')
    encoded_vars = ohe.fit_transform(df[categorical_cols]).toarray()
    encoded_vars_df = pd.DataFrame(encoded_vars, columns=ohe.get_feature_names_out(categorical_cols))

    print(df[categorical_cols])
    print("="*10)
    print(encoded_vars_df)
    print("="*10)

    # Processa os dados do formulário e faz previsões usando o modelo
    # Retorna as previsões como JSON
    # resultado = modelo.predict([data])[0]
    
    # if resultado < 0.0:
    #     resultado = 0.0
    
    resultado = 0.0
    
    return jsonify({'previsao': resultado})

if __name__ == '__main__':
    app.run(debug=True)
