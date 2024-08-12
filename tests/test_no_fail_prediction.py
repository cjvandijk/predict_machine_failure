import requests

"""
Tests the machine failure prediction service by sending it a list of machine
readings to get a response with likelihood of machine failure. This test has
readings that should produce a low failure likelihood.

Requires that the predict-machine-failure flask service is running
on port 9696.

This test can be executed by running it as a python script, e.g.,
`python test_no_fail_prediction.py` or
`pipenv run python test_no_fail_prediction.py`
"""

machine_readings = {
    "footfall": 83,
    "temp_mode": 4,
    "air_quality": 3,
    "proximity_sensor": 4,
    "current_usage": 6,
    "voc_level": 1,
    "revolutions_per_minute": 28,
    "input_pressure": 6,
    "temperature": 8,
}

url = "http://localhost:9696/predict"

response = requests.post(url, json=machine_readings)
resp = response.json()
print(resp)
assert "error_message" in resp
assert resp["error_message"] is None
assert "failure_likelihood" in resp
