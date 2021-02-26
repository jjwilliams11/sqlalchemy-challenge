# Import all dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

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

# Setup Flask Routes

@app.route("/")
def home():
    """List all routes that are available.""" 
    return (
        f"Welcome to Hawaii's weather API!<br/>"
        f"The available routes for you to explore are below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )



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


@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year."""
    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    precipitation_query = session.query(measurement.date, measurement.tobs).all()

    #Close session link
    session.close()

    # Create a dictionary from the row data and append to a list precipitations
    hawaii_temps = []

    for date, tobs in precipitation_query:
        hawaii_tobs_dict = {}
        hawaii_tobs_dict["date"] = date
        hawaii_tobs_dict["tobs"] = tobs
        hawaii_temps.append(hawaii_tobs_dict)
    
    return jsonify(hawaii_temps)




# most_active_station = stations_count.iloc[0].station
# station_stats_query = session.query(measurement.station, func.min(measurement.tobs),
#                                     func.max(measurement.tobs), func.avg(measurement.tobs),
#                                    func.count(measurement.tobs))\
#                                     .filter(measurement.station == most_active_station).statement
# station_temp = pd.read_sql_query(station_stats_query,session.bind)
# station_temp

# temp_query = session.query(measurement.date, measurement.tobs)\
#     .filter(measurement.date.between(end_date, start_date))\
#     .filter(measurement.station == most_active_station).statement


@app.route("/api/v1.0/<start>")
def start(start = None):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all 
    dates greater than and equal to the start date."""

    #Create a session to link from Python to DB
    session = Session(engine)

    #Query all precipatations for Hawaii
    start_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs) )\
                            .filter( measurement.date >= start)\
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



@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Code"""


if __name__ == '__main__':
    app.run(debug=True)