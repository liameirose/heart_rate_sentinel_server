from pymodm import connect
from pymodm import MongoModel, fields
from flask import Flask, jsonify, request


# connect("mongodb://liameirose:sharoniscool8@ds037283.mlab.com:37283/bme590")
#
#
# class User(MongoModel):
#     email = fields.EmailField(primary_key=True)
#     patient_id = fields.CharField()
#     user_age = fields.CharField()
#     heart_rate = fields.CharField()


app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    patient = {
        "patient_id": r[0, 1],
        "attending email": r[1, 1],
        "user age": r[2, 1]
    }
    return jsonify(patient)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    r = request.get_json()
    patient_hr = {
        "patient_id": r[0, 1],
        "heart_rate": r[1, 1],
    }
    return jsonify(patient_hr)

  

