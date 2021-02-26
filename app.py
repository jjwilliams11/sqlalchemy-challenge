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




@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""



@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year."""



@app.route("/api/v1.0/<start>")
def start():
    """Code"""



@app.route("/api/v1.0/<start>/<end>")
def start_end():
    """Code"""


if __name__ == '__main__':
    app.run(debug=True)