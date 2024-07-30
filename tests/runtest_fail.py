import requests

"""
Tests the machine failure prediction service by sending it a list of machine
readings to get a response with likelihood of machine failure. This test has
readings that should produce a high failure likelihood.

Requires that the predict-machine-failure flask service is running
on port 9696.

This test is not executed through pytest, but by running it as a python script,
e.g. `python runtest_fail.py` or `pipenv run python runtest_fail.py`
"""

machine_readings = {
    "footfall": 15,
    "temp_mode": 3,
    "air_quality": 7,
    "proximity_sensor": 1,
    "current_usage": 6,
    "voc_level": 5,
    "revolutions_per_minute": 45,
    "input_pressure": 6,
    "temperature": 22,
}

url = "http://localhost:9696/predict"

response = requests.post(url, json=machine_readings)
print(response.json())
