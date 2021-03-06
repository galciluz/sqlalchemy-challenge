import numpy as np
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    
    session = Session(engine)
    # search for the previous year
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date2 = recent_date.date
    last_date=session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    date1 = last_date.date
    
    session.close()
    """List all available api routes."""
    return (
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation in the last 12 month:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations: <br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"temperature observations (TOBS) for the previous year for the most active station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date(YYYY-MM-DD):<br/> "
        f"/api/v1.0/start<br/>"
        f"<br/>"
        f"Calculates the MIN/AVG/MAX temperature for dates  between start date and end date (YYYY-MM-DD):<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/>"
        f"Dates between: " + date1 + " to "+ date2 + "<br/>"
    )
    
#Return the JSON representation of precipitation in the last 12 month.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # search for the previous year
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date1 = recent_date.date
    date1 = datetime.strptime(date1, '%Y-%m-%d').date()
    date2 = date1 - dt.timedelta(days=365)

    # Query to select all the percipitacion in the previous year 
    prcpresults = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= date2).\
            order_by(Measurement.date.desc()).all()

    session.close()
    # Create a dictionary from the row data and append to a list of precipitation
    prcplist = []
    for date, prcp in prcpresults:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        prcplist.append(precipitation_dict)

    return jsonify(prcplist)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query  all station
    stat = session.query(Station.station, Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    stationlist = []
    for station,name,latitude,longitude,elevation in stat:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stationlist.append(station_dict)

    return jsonify(stationlist)

#Return a JSON list of temperature observations (TOBS) for the previous year for the most active station.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # search for the previous year
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date1 = recent_date.date
    date1 = datetime.strptime(date1, '%Y-%m-%d').date()
    date2 = date1 - dt.timedelta(days=365)
    
    # Query to find the most activate station  
    stationact = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).\
            order_by(func.count(Measurement.date).desc()).first()

    # Query to select all the tobs measure in the last year
    stationtobs = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == stationact.station).\
            filter(Measurement.date >=date2).\
            order_by(Measurement.date.desc()).all()
        
    session.close()

    toblist = []
    for date, tobs in stationtobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        toblist.append(tobs_dict)

    return jsonify(toblist)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date.
@app.route("/api/v1.0/<start>")
def stationstart(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    
    # Query to find calculate `TMIN`, `TAVG`, and `TMAX`
    summary = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >=start).all()
        
    session.close()

    # Convert list of tuples into normal list
    summarylist = list(np.ravel(summary))

    return jsonify(summarylist)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date and end date.
@app.route("/api/v1.0/<start>/<end>")
def stationstartend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end = dt.datetime.strptime(end, '%Y-%m-%d').date()
   
    # Query to find calculate `TMIN`, `TAVG`, and `TMAX`
    summary = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
            filter(Measurement.date >= start ).filter(Measurement.date <= end).all()
        
    session.close()

    # Convert list of tuples into normal list
    summarylist = list(np.ravel(summary))

    return jsonify(summarylist)

if __name__ == '__main__':
    app.run(debug=True)