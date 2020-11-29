import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
inspector = inspect(engine)
inspector.get_table_names()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

def temp_info(parameter_list):

    session = Session(engine)

    start_date = dt.datetime.strptime(parameter_list[0], '%Y-%m-%d')

    end_date = session.query(func.max(Measurement.date)).first()
    end_date = end_date[0]

    if len(parameter_list) > 1:
        end_date = parameter_list[1]

    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

    observations = []
    obs_dict = {}
    obs_dict['start date'] = start_date
    obs_dict['end date'] = end_date

    if start_date > end_date:
        obs_dict['error'] = 'problem with dates'
        observations.append(obs_dict)
        session.close()
        return observations,400

    sel = [func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]

    temp_averages = session.query(*sel).\
            filter(Measurement.date >= start_date).\
                filter(Measurement.date  <= end_date).all()
    session.close()
    
    observations.append(obs_dict)
    for tmin ,tmax, tavg  in temp_averages:
        obs_dict = {}
        obs_dict['TMIN'] = tmin
        obs_dict['TMAX'] = tmax
        obs_dict['TAVG'] =  tavg
        observations.append(obs_dict)

    return observations,200

    
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    precipitations = []
    for date,prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precipitations.append(precip_dict)

    return jsonify(precipitations)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    maxdate = session.query(func.max(Measurement.date)).first()
    print(maxdate)
    querydate = dt.datetime.strptime(maxdate[0] , '%Y-%m-%d') - dt.timedelta(days = 365)

    active_station  = session.query(Measurement.station).\
                        group_by(Measurement.tobs).\
                            order_by(func.count(Measurement.tobs).desc()).first()

    results = session.query(Measurement.date,Measurement.tobs,Station.name).\
                filter(Measurement.station == Station.station).\
                filter(Measurement.date >= querydate).\
                    filter(Measurement.station == active_station[0]).all()

    session.close()

    tobs  = [result[1] for result in results[:]]
    
    # Convert list of tuples into normal list
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def only_start_date_avaliable__start(start):

    start_date = start.replace(" ", "")

    parameter_list = [start_date]
    
    observations = temp_info(parameter_list)

    return jsonify(observations)


@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end=None):

    parameter_list=[]
    
    parameter_list.append(start.replace(" ", ""))
    
    parameter_list.append(end.replace(" ", ""))

    print(parameter_list)

    observations = temp_info(parameter_list)

    return jsonify(observations)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)