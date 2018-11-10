import requests


def post_patients(info):
    r = requests.post("http://bme590.suyash.io/student", json=info)
    result = r.json()


def main():
   info = {
    "patient_id": "1",
    "attending email": "Meirose",
    "user_age": 50,
    "heart_rate": 100,
    }
    post_patients(info)


if __name__ == "__main__":
    main()
