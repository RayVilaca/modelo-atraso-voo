
import pickle
import warnings
import pandas as pd
from flask import Flask, render_template, request, jsonify

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
        'CRSDepTime',
        'ArrTime',
        'AirTime',
        'Year',
        'DOT_ID_Marketing_Airline',
        'Flight_Number_Marketing_Airline',
        'DOT_ID_Operating_Airline',
        'OriginAirportID',
        'OriginCityMarketID',
        'OriginStateFips',
        'OriginWac',
        'DestAirportID',
        'DestCityMarketID',
        'DestStateFips',
        'DestWac',
        'DepDel15',
        'DepartureDelayGroups',
        'TaxiOut',
        'TaxiIn',
        'CRSArrTime',
        'ArrDel15',
        'DivAirportLandings',
        'Airline_American Airlines Inc.',
        'Airline_Delta Air Lines Inc.',
        'Airline_SkyWest Airlines Inc.',
        'Airline_Southwest Airlines Co.',
        'Airline_United Air Lines Inc.',
        'DayofMonth_1',
        'DayofMonth_2',
        'DayofMonth_3',
        'DayofMonth_4',
        'DayofMonth_5',
        'DayofMonth_6',
        'DayofMonth_7',
        'DayofMonth_8',
        'DayofMonth_9',
        'DayofMonth_10',
        'DayofMonth_11',
        'DayofMonth_12',
        'DayofMonth_13',
        'DayofMonth_14',
        'DayofMonth_15',
        'DayofMonth_16',
        'DayofMonth_17',
        'DayofMonth_18',
        'DayofMonth_19',
        'DayofMonth_20',
        'DayofMonth_21',
        'DayofMonth_22',
        'DayofMonth_23',
        'DayofMonth_24',
        'DayofMonth_25',
        'DayofMonth_26',
        'DayofMonth_27',
        'DayofMonth_28',
        'DayofMonth_29',
        'DayofMonth_30',
        'DayofMonth_31',
        'DayOfWeek_1',
        'DayOfWeek_2',
        'DayOfWeek_3',
        'DayOfWeek_4',
        'DayOfWeek_5',
        'DayOfWeek_6',
        'DayOfWeek_7',
        'Quarter_1',
        'Quarter_2',
        'Quarter_3',
        'Quarter_4']

    df = pd.DataFrame([data[0:-4] + [0] * 47], columns=columns)
    
    df[data[-4]] = 1
    df[data[-3]] = 1
    df[data[-2]] = 1
    df[data[-1]] = 1
    
    print(df.info())
    
    # Processa os dados do formulário e faz previsões usando o modelo
    # Retorna as previsões como JSON
    resultado = modelo.predict([df.iloc[0]])[0]
    
    if resultado < 0.0:
        resultado = 0.0
    
    return jsonify({'previsao': resultado})

if __name__ == '__main__':
    app.run(debug=True)
