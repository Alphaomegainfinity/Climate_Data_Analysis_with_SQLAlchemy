#setup dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask
from flask import jsonify


#Database setup:
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

# Flask setup
app = Flask(__name__)

#Flask Routes:

#creating homepage:
@app.route("/")
def homepage():
    """All available api routes"""
    return (
        f"Welcome to the Hawaii API Home Page!<br/>"
        f"All available Routes as below:<br>"
        f"Precipitation measurement from the last 12 months: /api/v1.0/precipitation<br>"
        f"A list of all stations from dataset: /api/v1.0/stations<br>"
        f"Date and Temperature observations query of the most active station for the past 12 months: /api/v1.0/tobs<br>"
        f"Retrieve the minimum, maximum, and average temperatures from  the start date (YYYY-MM-DD) onward: /api/v1.0/<start><br>"
        f"Retrieve the minimum, maximum, and average temperatures from the start date to end date(start/end) (YYYY-MM-DD): /api/v1.0/<start>/<end><br>"
    )

#creating /api/v1.0/precipitation

@app.route ("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    retrieve_data = session.query(measurement.prcp, str(measurement.date)).filter(measurement.date > '2016-08-22')\
        .filter(measurement.date <= '2017-08-23').order_by(measurement.date).all()

    session.close()
    #convert list of tuples into normal list
    retrieve_list = list(np.ravel(retrieve_data))
    #convert to json
    return jsonify (retrieve_list)

#creating a list of stations:

@app.route ("/api/v1.0/stations")
def stations():
    session = Session(engine)
    number_stations = session.query(station.station,station.name).all()

    session.close()
    #convert list of tuples into normal list
    stations_list = list(np.ravel(number_stations))
    #convert to json
    return jsonify (stations_list)

#creating a list of date and temperature of the most active station for the previous year of data

@app.route ("/api/v1.0/tobs")
def temp_ob():
    session = Session(engine)
    active_stations = session.query(measurement.station, measurement.date, measurement.tobs).filter(measurement.date > '2016-08-22')\
        .filter(measurement.date <= '2017-08-23').filter(measurement.station == "USC00519281").order_by(measurement.date).all()

    session.close()
    #convert list of tuples into normal list
    active_stations_list= list(np.ravel(active_stations))
    #convert to json
    return jsonify (active_stations_list)


#creating a list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
@app.route("/api/v1.0/<start>")
def tob_start(start):
    session = Session(engine)
    
    query_tob = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))

    query_tob = query_tob.filter(measurement.date >= start).all()

    session.close()
    #convert list of tuples into normal list
    query_tob_list= list(np.ravel(query_tob))
    #convert to json
    return jsonify (query_tob_list)


#creating a list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
@app.route("/api/v1.0/<start>/<end>")
def tob_start_end(start,end):
    session = Session(engine)
    
    query_tob = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))

    query_tob = query_tob.filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()
    #convert list of tuples into normal list
    query_tob_list= list(np.ravel(query_tob))
    #convert to json
    return jsonify (query_tob_list)

if __name__ == '__main__':
    app.run (debug=True)