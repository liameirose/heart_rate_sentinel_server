import requests


def post_new_patient():
    r = requests.post("http://0.0.0.0:5000/api/new_patient", json={
                        "patient_id": 6,
                        "attending_email": "liacmeirose@gmail.com",
                        "user_age": 2,
                        "heart_rate": 155.0
                        })
    patient_result = r.json()


def post_hr():
    r = requests.post("http://0.0.0.0:5000/api/heart_rate", json={
                        "patient_id": 9,
                        "attending_email": "liacmeirose@gmail.com",
                        "user_age": 2,
                        "heart_rate": 155.0
                        })
    patient_result = r.json()


def post_interval():
    r = requests.post("http://0.0.0.0:5000/api/heart_rate/interval_average",
                      json={
                            "patient_id": 1,
                            "interval": "2018-03-09 11:00:36.372339"
                            })
    patient_result = r.json()


if __name__ == "__main__":
    post_new_patient()
    post_hr()
    post_interval()
