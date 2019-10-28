# Created By: Mandar R. Gogate
# Created On: 10/28/2019
# References:
# https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
# https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
# https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa/48234567
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app = Flask(__name__)

dbPath = "hawaii.sqlite"
engine = create_engine("sqlite:///" + dbPath)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= "2016-08-23").order_by(Measurement.date.desc()).all()
    session.close()
    return jsonify(dict(results))


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station)\
        .group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    session.close()
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281", Measurement.date >= "2016-08-23").all()
    session.close()
    return jsonify(dict(results))


@app.route("/api/v1.0/<start>")
# http://127.0.0.1:5000/api/v1.0/2017-01-01
def getDataByStartDate(start):    
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()        
    session.close()
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
# http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-01-07
def getDataByStartAndEndDate(start, end):    
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()    
    session.close()
    return jsonify(results)

# http://127.0.0.1:5000/
@app.route("/")
def hello():
    message="""<table>
                <tr>
                    <td>precipitation</td>
                    <td>/api/v1.0/precipitation</td>
                </tr>
                <tr>
                    <td>stations</td>
                    <td>/api/v1.0/stations</td>
                </tr>
                <tr>
                    <td>tobs</td>
                    <td>/api/v1.0/tobs</td>
                </tr>
                <tr>
                    <td>Start Date</td>
                    <td>/api/v1.0/[start]</td>
                </tr>
                <tr>
                    <td>Start And End Date</td>
                    <td>/api/v1.0/[start]/[end]</td>
                </tr>
                </table>
                """
    return message


if __name__ == "__main__":
    app.run(debug=True)
