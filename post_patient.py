import requests


def post_patient():
    r = requests.post("http://127.0.0.1:5000/", json={
        "patient_id": 1,
        "attending_email": "liameirose@meirose.com",
        "user_age": 24,
        "heart_rate": 80
    })
    patient_result = r.json()
    return patient_result







