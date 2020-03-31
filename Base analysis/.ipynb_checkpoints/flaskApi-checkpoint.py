# Week 10 SqlAlchemy hwk

### Dependencies ### 
from flask import Flask
from flask import jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from datetime import datetime

# Starter code for flask
app = Flask(__name__)
    
# Connecting to Database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

# References to each table in the database
Measurement = Base.classes.measurement
Station = Base.classes.station

# Welcome - Home Page
@app.route('/')
def welcome():
    return """
    The following routes are available:<br /><br />
    /api/v1.0/precipitation - returns all precipitation values in the last year<br /><br />
    /api/v1.0/stations - returns all available stations<br /><br />
    /api/v1.0/tobs - returns all temperature observations in the last year<br /><br />
    /api/v1.0/start - start must be entered in dd/mm/yyyy format - returns min/max/avg temp<br /><br />
    /api/v1.0/start/end - dates must be entered in dd/mm/yyyy format - returns min/max/temp over the date range<br /><br />
    """


@app.route('/api/v1.0/precipitation')
def display_precipitation():
    session = Session(engine)
    date = dt.datetime(2016,8,23)
    last_yr = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date)
    prcp_dict = {}
    for x in last_yr:
        prcp_dict[x[0]] = x[1]
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def display_stations():
    session = Session(engine)
    stations = session.query(Measurement.station, Measurement.tobs)
    stationsDF = pd.DataFrame(stations)
    unique_station = stationsDF['station'].unique()
    station_dict = {}  
    for index,val in enumerate(unique_station):
        station_dict[index] = val
    return jsonify(station_dict)

@app.route('/api/v1.0/tobs')
def display_temps():
    session = Session(engine)
    date = dt.datetime(2016,8,23)
    stations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date)
    stationsDF = pd.DataFrame(stations)
    stationsDF = stationsDF.dropna()
    tobs_dict = {}
    for x in stations:
        tobs_dict[x[0]] = x[1]
    return jsonify(tobs_dict)

@app.route('/api/v1.0/<start>')
def start_temps(start):
    start_date = datetime.strptime('{}'.format(start), '%m-%d-%Y')
    start_date = str(start_date)
    start_date = start_date[:11]
    session = Session(engine)
    temperatures = session.query(Measurement.tobs).filter(Measurement.date >= start_date)
    tempsDf = pd.DataFrame(temperatures)
    min_temp = tempsDf['tobs'].min()
    max_temp = tempsDf['tobs'].max()
    avg_temp = tempsDf['tobs'].mean()
    temp_dict1 = {
        'Max Temp': max_temp,
        'Min Temp': min_temp,
        'Avg Temp': avg_temp,
    }
    return jsonify(temp_dict1)

@app.route('/api/v1.0/<start>/<end>')
def date_range_temps(start,end):
    start_date = datetime.strptime('{}'.format(start), '%m-%d-%Y')
    start_date = str(start_date)
    start_date = start_date[:11]
    end_date = datetime.strptime('{}'.format(end), '%m-%d-%Y')
    end_date = str(end_date)
    end_date = end_date[:11]
    session = Session(engine)
    temperatures = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)
    tempsDf = pd.DataFrame(temperatures)
    min_temp = tempsDf['tobs'].min()
    max_temp = tempsDf['tobs'].max()
    avg_temp = tempsDf['tobs'].mean()
    temp_dict2 = {
        'Max Temp': max_temp,
        'Min Temp': min_temp,
        'Avg Temp': avg_temp,
    }
    return jsonify(temp_dict2)

# Starter code for flask
if __name__ == "__main__":
    app.run(debug=True)