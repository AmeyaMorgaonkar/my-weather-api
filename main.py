from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():

    df1 = pd.read_csv('data_small/stations.txt', skiprows=17)

    station_id = []
    stations = []

    for i in range(len(df1)):
        station_id.append(df1['STAID'][i])
        stations.append(df1['STANAME                                 '][i].strip(" "))

    no_of_stations = len(stations)

    return render_template('home.html', stations=stations, station_id=station_id, no_of_stations=no_of_stations)



@app.route('/api/<station>/<date>')
def data(station, date):
    
    df = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt", skiprows=20, parse_dates=["    DATE"])
    df1 = pd.read_csv('data_small/stations.txt', skiprows=17)

    station_name = df1.loc[df1['STAID'] == int(station)]['STANAME                                 '].squeeze().strip(" ")

    return render_template('weather.html', station=station, station_name=station_name, date=date, temp=str(df.loc[df['    DATE'] == date]['   TG'].squeeze()/10))


@app.errorhandler(404)
def file_not_found(e):
    return "Data not found for the given station. Please refer to the available stations on home page."


if __name__ == '__main__':
    app.run(debug=True, port=5000)