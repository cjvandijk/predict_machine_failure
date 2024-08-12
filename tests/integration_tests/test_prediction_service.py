import requests

"""
Tests the machine failure prediction service by sending it a list of machine
readings to get a response with likelihood of machine failure. This test has
readings that should produce a high failure likelihood.

Requires that the predict-machine-failure flask service is running
on port 9696.

This test can be executed by running it as a python script, e.g.,
`python test_fail_prediction.py` or
`pipenv run python test_fail_prediction.py`
"""

url = "http://localhost:9696/predict"

machine_readings = {
    "should_predict_failure": {
        "footfall": 15,
        "temp_mode": 3,
        "air_quality": 7,
        "proximity_sensor": 1,
        "current_usage": 6,
        "voc_level": 5,
        "revolutions_per_minute": 45,
        "input_pressure": 6,
        "temperature": 22,
    },
    "should_not_predict_failure": {
        "footfall": 83,
        "temp_mode": 4,
        "air_quality": 3,
        "proximity_sensor": 4,
        "current_usage": 6,
        "voc_level": 1,
        "revolutions_per_minute": 28,
        "input_pressure": 6,
        "temperature": 8,
    },
    "should_send_error_msg": {
        "footfall": 3000000,
        "temp": -19,
        "aqi": 3,
    },
}

for k in machine_readings:
    response = requests.post(url, json=machine_readings[k])
    resp = response.json()

    assert "error_message" in resp
    assert "failure_likelihood" in resp

    if k == "should_predict_failure":
        assert int(resp["failure_likelihood"][:-2]) <= 50

    if k == "should_not_predict_failure":
        assert int(resp["failure_likelihood"][:-2]) > 50

    if k == "should_send_error_msg":
        assert resp["error_message"] is not None
    else:
        assert resp["error_message"] is None

    print("*** All tests for the prediction web service have passed ***")
