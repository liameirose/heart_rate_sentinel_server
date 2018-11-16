from pymodm import connect
from pymodm import MongoModel, fields
from flask import Flask, jsonify, request
from datetime import datetime
import numpy as np
import sendgrid
import os
from sendgrid.helpers.mail import *

connect("mongodb://liameirose:sharoniscool8@ds037283.mlab.com:37283/bme590")
app = Flask(__name__)


class User(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    user_age = fields.IntegerField()
    email = fields.EmailField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    hr_times = fields.ListField(field=fields.DateTimeField())


def validate_input(r):
    """
    Function returns a boolean showing whether the user input
    is complete and in the correct form.

    Args:
        r: json dictionary input

    Returns:
        boolean: states whether user input is valid or not.
    """
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
            print("Invalid input: 'user_age' must be an integer."
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
    """
    Function appends additional heart rates to an existing patient.

    Args:
        patient_id: integer corresponding to a certain patient
        hr: heart rate of patient
        time: date and time when heart rate is input into the server

    Returns:
        Saves new heart rate information to existing patient.
    """
    user = User.objects.raw({"_id": patient_id}).first()
    user.heart_rate.append(hr)
    user.hr_times.append(time)
    user.save()


def new_user(patient_id, email, user_age, hr, time):
    """
    Function creates a new patient with given information.

    Args:
        patient_id: integer corresponding to a certain patient
        email: the email of the patient's attending physician
        user_age: age of the patient
        hr: heart rate of patient
        time: dat and time when heart rate is input into the server

    Returns:
        Saves new heart rate information to a new user.
    """
    u = User(patient_id, user_age, email, [], [])
    u.heart_rate.append(hr)
    u.hr_times.append(time)
    u.save()


def give_hr(patient_id):
    """
    Function returns heart rate values for a given patient.

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        Heart rate values from patient
    """
    u = User.objects.raw({"_id": patient_id}).first()
    return u.heart_rate


def give_age(patient_id):
    """
    Function returns the age for a given patient.

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        Age of a patient
    """
    u = User.objects.raw({"_id": patient_id}).first()
    return u.user_age


def give_time(patient_id):
    """
    Function returns the list of times corresponding to certain heart rates.

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        List of heart rate times
    """
    u = User.objects.raw({"_id": patient_id}).first()
    return u.hr_times


def give_avg(hr_list):
    """
    Function returns the average heart rate for a given patient.

    Args:
        hr_list: list of heart rate values

    Returns:
        avg: average heart rate of patient
    """
    avg = np.mean(hr_list)
    return avg


def avg_interval(hr, times, interval):
    """
    Function returns the average over a user given interval.

    Args:
        hr: list of heart rates of patient
        times: list of times from patient
        interval: date and time from which the average will be calculated

    Returns:
        avg_from: average heart rate of patient from given time interval
    """
    try:
        time_from = datetime.strptime(interval, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return "Time interval is not in the right format. Please try again."

    hr_from = []

    for n, t in enumerate(times):
        if t > time_from:
            hr_from.append(hr[n])
    avg_from = give_avg(hr_from)
    return avg_from


def tachy(user_age, heart_rate):
    """
    Function states if the patient is tachycardic.

    Args:
        user_age: age of certain patient
        heart_rate: latest heart rate of patient

    Returns:
        Statement which indicated whether the patient is tachycardic or not.
    """
    if user_age >= 1 and user_age <= 2 and heart_rate > 151:
        return True
    elif user_age >= 3 and user_age <= 4 and heart_rate > 137:
        return True
    elif user_age >= 5 and user_age <= 7 and heart_rate > 133:
        return True
    elif user_age >= 8 and user_age <= 11 and heart_rate > 130:
        return True
    elif user_age >= 12 and user_age <= 15 and heart_rate > 119:
        return True
    elif user_age >= 15 and heart_rate > 130:
        return True
    else:
        return False


def send_email(attending_email, id):
    """
    Function sends an email and returns a confirmation statement.

    Args:
        attending_email: email of patient's attending
        id: id corresponding to a certain patient

    Returns:
        Statement stating the email was sent.
    """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("liacmeirose@gmail.com")
    to_email = Email(attending_email)
    subject = "Patient is tachycardic"
    content = Content("text/plain", "Patient " + str(id) + " is tachycardic")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return "Email sent."


@app.route("/test", methods=["GET"])
def test():
    """
    Function to test working server

    Returns:
        Test statement.
    """
    return "Hello, this is a test"


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """
    Function posts a new patient to the web server.
    If a patient is tachycardic, an email is sent.

    Returns:
        .json file containing new patient information
    """
    r = request.get_json()
    good = validate_input(r)
    if good is True:
        pat_id = r["patient_id"]
        email = r["attending_email"]
        age = r["user_age"]
        hr = r["heart_rate"]
        time = datetime.now()
        oh_no = tachy(age, hr)
        new_user(pat_id, email, age, hr, time)
        if oh_no is True:
            send_email(email, pat_id)
            print("Tachycardic")
        print("New patient, responses recorded")
        return jsonify(pat_id, email, age)
    else:
        return "Invalid input."


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """
    Function posts a new heart rate reading to a server.
    It will either append it to an existing user or create
    a new user.
    If a patient is tachycardic, an email is sent.

    Returns:
        .json file containing the patient heart rate information
    """
    r = request.get_json()
    good = validate_input(r)
    if good is True:
        pat_id = r["patient_id"]
        email = r["attending_email"]
        age = r["user_age"]
        hr = r["heart_rate"]
        oh_no = tachy(age, hr)
        time = datetime.now()
        print(oh_no)
        if oh_no is True:
            send_email(email, pat_id)
            print("Tachycardic")
        try:
            append_hr(pat_id, hr, time)
            print("Patient exists, responses recorded")
            return jsonify(pat_id, hr)
        except:
            new_user(pat_id, email, age, hr, time)
            if oh_no == "Tachycardia  detected.":
                send_email(email, pat_id)
            print("Patient did not exist, a new patient was created")
            return jsonify(pat_id, hr)
    else:
        return "Invalid input."


@app.route("/api/status/<patient_id>", methods=["GET"])
def status(patient_id):
    """
    Function gets the status of a certain patient

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        .json file stating if the patient has tachycardia
    """
    patient_id = int(patient_id)
    age = give_age(patient_id)
    hr = give_hr(patient_id)[-1]
    time = give_time(patient_id)[-1]
    try:
        output = tachy(age, hr)
        print(output)
        if output is True:
            msg = "Patient is tachycardic"
            return jsonify(msg, time)
        else:
            msg = "Patient is not tachycardic"
            return jsonify(msg, time)
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def all_hr(patient_id):
    """
    Function gets the heart rate list of a certain patient

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        .json file of all of the patient heart rates
    """
    patient_id = int(patient_id)
    hr = give_hr(patient_id)
    try:
        return jsonify(hr)
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def find_avg(patient_id):
    """
    Function gets the average heart rate of a certain patient

    Args:
        patient_id: integer corresponding to a certain patient

    Returns:
        .json file of the average heart rate
    """
    patient_id = int(patient_id)
    hr = give_hr(patient_id)
    try:
        return jsonify(give_avg(hr))
    except:
        return "Patient information does not exist"


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def average_over_interval():
    """
    Function posts the average heart rate from a certain interval.

    Returns:
        .json file containing average heart rate
    """
    r = request.get_json()
    pat_id = r["patient_id"]
    hr = give_hr(pat_id)
    times = give_time(pat_id)

    interval = r["interval"]
    try:
        result = avg_interval(hr, times, interval)
        print(result)
        return jsonify(result)
    except Exception as inst:
        print(inst)
        return "Patient information does not exist."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5008)
