# Import all dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

from flask import Flask, jsonify

# Setup database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Setup Flask

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False - stops the jsonify from resetting order to alphabetical

# Setup Flask Routes
# Home Route with Text
@app.route("/")
def home():
    """List all routes that are available.""" 
    return (
        f"Welcome to Hawaii's weather API which provides data for 2010-01-01 to 2017-08-23<br/>"
        f"The available routes for you to explore are below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"

    )

# Precipation Route with all dates and precipiation measures
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    Return the JSON representation of your dictionary."""
    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    precipitation_query = session.query(measurement.date, measurement.prcp).all()

    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    hawaii_precip = []

    for date, prcp in precipitation_query:
        hawaii_prcp_dict = {}
        hawaii_prcp_dict["date"] = date
        hawaii_prcp_dict["prcp"] = prcp
        hawaii_precip.append(hawaii_prcp_dict)
    
    return jsonify(hawaii_precip)


# Station Route with all Hawaii stations
@app.route("/api/v1.0/stations")
def stations():
    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    stations_query = session.query(station.station, station.name,
                                    station.latitude, station.longitude, 
                                    station.elevation).all()

    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    hawaii_station_list = []

    for stations, names, latitude,longitude,elevation in stations_query:
        hawaii_station_dict = {}
        hawaii_station_dict["station"] = stations
        hawaii_station_dict["name"] = names
        hawaii_station_dict["latitude"] = latitude
        hawaii_station_dict["longitude"] = longitude
        hawaii_station_dict["elevation"] = elevation
        hawaii_station_list.append(hawaii_station_dict)
    
    return jsonify(hawaii_station_list)

# Temperature Route with temperatures for the most active station for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    
    #Create a session to link from Python to DB
    session = Session(engine)

    # Find the most recent date in the data set and 
    max_query = session.query(func.max(measurement.date)).one()
    max_date = max_query[0]

    # Convert date string to datetime for start date
    max_date_conv = dt.datetime.strptime(max_date, '%Y-%m-%d')
    start_date = max_date_conv.date()


    # Calculate the date one year from the last date in data set.
    days_in_year = dt.timedelta(365)
    end_date = start_date - days_in_year

    #Determine most active station for query
    active_station_query = session.query(measurement.station, func.count(measurement.station))\
            .group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()

    most_active_station = active_station_query[0]
    
    station_temp_query = session.query(measurement.station, measurement.date, measurement.tobs)\
                    .filter(measurement.station == most_active_station)\
                    .filter(measurement.date.between(end_date, start_date))


    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    hawaii_temps = []

    for station, date, tobs in station_temp_query:
        hawaii_tobs_dict = {}
        hawaii_tobs_dict["station"] = station
        hawaii_tobs_dict["date"] = date
        hawaii_tobs_dict["tobs"] = tobs
        hawaii_temps.append(hawaii_tobs_dict)
    
    return jsonify(hawaii_temps)


# Start Route with Min, Max, and AVG from all dates after the start date given 
@app.route("/api/v1.0/<start>")
def start(start = None):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all 
    dates greater than and equal to the start date."""

    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    start_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs) )\
                            .filter(measurement.date >= start)\
                            .group_by(measurement.date)


    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    start_search = []

    for date, min, max, avg in start_query:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_search.append(start_dict)
    
    return jsonify(start_search)


# Start/End Route with Min, Max, and AVG from all dates between dates given
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None ,end = None):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all 
    dates between the start and end dates."""

    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    start_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs) )\
                            .filter(measurement.date.between(start, end))\
                            .group_by(measurement.date)


    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    start_search = []

    for date, min, max, avg in start_query:
        start_dict = {}
        start_dict["date"] = date
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_search.append(start_dict)
    
    return jsonify(start_search)

if __name__ == '__main__':
    app.run(debug=True)