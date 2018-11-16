from hr_sentinel_server import validate_input, give_avg
from hr_sentinel_server import tachy, send_email, avg_interval
from datetime import datetime


def test_validate_input():
    fake1 = {
        "patient_id": 2,
        "attending_email": "suyash@suyashkumar.com",
        "user_age": 50,
        "heart_rate": 100.0
    }

    output1 = validate_input(fake1)
    assert output1 is True

    fake2 = {
        "patient_id": 2,
        "attending_email": "liameirose@liameirose.com",
        "user_age": 60,
    }

    output2 = validate_input(fake2)
    assert output2 is False

    fake3 = {
        "patient_id": 2,
        "attending_email": 45,
        "user_age": 60,
        "heart_rate": 100.0
    }
    output3 = validate_input(fake3)
    assert output3 is False

    fake4 = {
        "patient_id": 2,
        "user_email": "suyash@suyashkumar.com",
        "user_age": "sixty",
        "heart_rate": 100.0
    }
    output4 = validate_input(fake4)
    assert output4 is False


def test_give_avg():
    fake_hr_list = [1, 2, 3, 4, 5, 6, 7, 8]
    fake_avg = give_avg(fake_hr_list)
    assert fake_avg == 4.5


def test_tachy():
    fake_age1 = 2
    fake_hr1 = 155
    tach1 = tachy(fake_age1, fake_hr1)
    assert tach1 == "Tachycardia detected."

    fake_age2 = 50
    fake_hr2 = 100
    tach2 = tachy(fake_age2, fake_hr2)
    assert tach2 == "No tachycardia detected."


def test_send_email():
    fake_email = "liacmeirose@gmail.com"
    pat_id = 88
    result = send_email(fake_email, pat_id)
    assert result == "Email sent."


def test_avg_interval():
    fake_times = ["2018-07-09 11:00:36.372339",
                  "2018-06-09 11:00:36.372339",
                  "2018-05-09 11:00:36.372339",
                  "2018-04-09 11:00:36.372339"]
    new = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')for x in fake_times]
    fake_hr = [1, 2, 3, 4]
    fake_interval = "2018-03-09 11:00:36.372339"
    result = avg_interval(fake_hr, new, fake_interval)
    assert result == 2.5
