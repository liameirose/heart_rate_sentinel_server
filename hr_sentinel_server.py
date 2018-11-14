from pymodm import connect
from pymodm import MongoModel, fields
from flask import Flask, jsonify, request
from datetime import datetime
import numpy as np


connect("mongodb://liameirose:sharoniscool8@ds037283.mlab.com:37283/bme590")
app = Flask(__name__)


class User(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    user_age = fields.IntegerField()
    email = fields.EmailField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    hr_times = fields.ListField(field=fields.DateTimeField())


def validate_input(r):
    try:
        int(r["patient_id"])
        if type(r["patient_id"]) is not int:
            print("Invalid input: 'patient_id' must be an integer.")
            return False
    except:
        print("No input provided for 'patient_id'. Please input information.")
        return False
    try:
        if type(r["attending_email"]) is not str:
            print("Invalid input: 'attending_email' input must be a string.")
            return False
    except:
        print("No input provided for 'attending_email'. "
              "Please input information.")
        return False
    try:
        int(r["user_age"])
        if type(r["user_age"]) is not int:
            print("Invalid input: 'user_age' must be an integer. "
                  "Server cannot be used for patients less than a year.")
            return False
    except:
        print("No input provided for 'user_age'. Please input information.")
        return False
    try:
        float(r["heart_rate"])
        if type(r["heart_rate"]) is not float:
            print("Invalid input: 'heart_rate' must be an float.")
            return False
    except:
        print("No input provided for 'heart rate'. Please input information.")
        return False
    print("Valid input")
    return True


def append_hr(patient_id, hr, time):
    user = User.objects.raw({"_id": patient_id}).first()
    user.heart_rate.append(hr)
    user.hr_times.append(time)
    user.save()


def new_user(patient_id, email, user_age, hr, time):
    u = User(patient_id, user_age, email, [], [])
    u.heart_rate.append(hr)
    u.hr_times.append(time)
    u.save()


def give_hr(patient_id):
    u = User.objects.raw({"_id": patient_id}).first()
    return u.heart_rate


def give_age(patient_id):
    u = User.objects.raw({"_id": patient_id}).first()
    return u.user_age


def give_time(patient_id):
    u = User.objects.raw({"_id": patient_id}).first()
    return u.hr_times


def give_avg(hr_list):
    avg = np.mean(hr_list)
    return avg


def avg_interval(patient_id, interval):
    try:
        time_from = datetime.strptime(interval, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return "Time interval is not in the right format. Please try again."
    hr = give_hr(patient_id)
    times = give_time(patient_id)

    hr_from = []

    for n, t in enumerate(times):
        if t > time_from:
            hr_from.append(hr[n])
    avg_from = give_avg(hr_from)
    return avg_from


def tachy(user_age, heart_rate):
    if user_age >= 1 and user_age <= 2 and heart_rate > 151:
        return "Tachycardia detected."
    elif user_age >= 3 and user_age <= 4 and heart_rate > 137:
        return "Tachycardia  detected."
    elif user_age >= 5 and user_age <= 7 and heart_rate > 133:
        return "Tachycardia detected."
    elif user_age >= 8 and user_age <= 11 and heart_rate > 130:
        return "Tachycardia  detected."
    elif user_age >= 12 and user_age <= 15 and heart_rate > 119:
        return "Tachycardia  detected."
    elif user_age >= 15 and heart_rate > 130:
        return "Tachycardia  detected."
    else:
        return 'No tachycardia detected.'


@app.route("/test", methods=["GET"])
def test():
    return "Hello, this is a test"


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    good = validate_input(r)
    if good is True:
        pat_id = r["patient_id"]
        email = r["attending_email"]
        age = r["user_age"]
        hr = r["heart_rate"]
        time = datetime.now()
        new_user(pat_id, email, age, hr, time)
        print("New patient, responses recorded")
        return jsonify(pat_id, email, age)
    else:
        return "Invalid input."


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    r = request.get_json()
    good = validate_input(r)
    if good is True:
        pat_id = r["patient_id"]
        email = r["attending_email"]
        age = r["user_age"]
        hr = r["heart_rate"]
        time = datetime.now()
        try:
            append_hr(pat_id, hr, time)
            print("Patient exists, responses recorded")
            return jsonify(pat_id, hr)
        except:
            new_user(pat_id, email, age, hr, time)
            print("Patient did not exist, a new patient was created")
            return jsonify(pat_id, hr)
    else:
        return "Invalid input."


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    patient_id = int(patient_id)
    age = give_age(patient_id)
    hr = give_hr(patient_id)[-1]
    time = give_time(patient_id)[-1]
    try:
        return jsonify(tachy(age, hr), time)
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def all_hr(patient_id):
    patient_id = int(patient_id)
    hr = give_hr(patient_id)
    try:
        return jsonify(hr)
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def find_avg(patient_id):
    patient_id = int(patient_id)
    hr = give_hr(patient_id)
    try:
        return jsonify(give_avg(hr))
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def average_over_interval():
    r = request.get_json()
    pat_id = r["patient_id"]
    interval = r["interval"]
    try:
        result = avg_interval(pat_id, interval)
        print(result)
        return jsonify(result)
    except:
        return "Patient information does not exist."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
