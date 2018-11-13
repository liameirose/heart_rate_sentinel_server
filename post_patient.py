import requests


def post_patient():
    # r = requests.post("http://127.0.0.1:5001/api/heart_rate", json={
    #     "patient_id": 1,
    #     "attending_email": "liameirose@meirose.com",
    #     "user_age": 24,
    #     "heart_rate": 82
    # })
    # patient_result = r.json()

    r = requests.post("http://127.0.0.1:5001/api/heart_rate/interval_average", json={
        "patient_id": 1,
        "interval": "2018-03-09 11:00:36.372339"
    })
    patient_result = r.json()

if __name__ == "__main__":
    post_patient()








