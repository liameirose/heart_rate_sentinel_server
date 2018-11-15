import requests


def post_patient():
    r = requests.post("http://127.0.0.1:5001/api/new_patient", json={
                        "patient_id": 6,
                        "attending_email": "liacmeirose@gmail.com",
                        "user_age": 2,
                        "heart_rate": 155.0
                        })
    patient_result = r.json()


if __name__ == "__main__":
    post_patient()
