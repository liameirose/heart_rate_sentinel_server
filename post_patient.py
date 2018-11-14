import requests


def post_patient():
    r = requests.post("http://127.0.0.1:5001/api/new_patient", json={
                        "patient_id": 2,
                        "attending_email": "liameirose@meirose.com",
                        "user_age": 24,
                        "heart_rate": 82.0
                        })
    patient_result = r.json()


if __name__ == "__main__":
    post_patient()
