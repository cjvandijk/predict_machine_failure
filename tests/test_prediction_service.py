"""
Tests the machine failure prediction service by sending it a list of machine
readings to get a response with likelihood of machine failure.

Requires that the predict-machine-failure flask service is running
on port 9696.

These tests can be executed with pytest from the root directory, e.g.,
`pipenv run pytest tests/test_fail_prediction.py`

or to run all tests in the tests directory:
`pipenv run pytest tests/`
"""

import requests


url = "http://localhost:9696/predict"


def test_response_should_predict_unlikely_failure():
    """
    Tests the machine failure prediction service by sending it a list of machine
    readings to get a response with likelihood of machine failure. This test has
    readings that should produce a low failure likelihood.
    """

    machine_reading = {
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
    
    response = requests.post(url, json=machine_reading)
    resp = response.json()
    
    assert "error_message" in resp
    assert resp["error_message"] is None
    assert "failure_likelihood" in resp
    assert int(resp["failure_likelihood"][:-2]) <= 50


def test_response_should_predict_likely_failure():
    """
    Tests the machine failure prediction service by sending it a list of machine
    readings to get a response with likelihood of machine failure. 
    """

    machine_reading = {
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
    
    response = requests.post(url, json=machine_reading)
    resp = response.json()
    
    assert "error_message" in resp
    assert resp["error_message"] is None
    assert "failure_likelihood" in resp
    assert int(resp["failure_likelihood"][:-2]) > 50


def test_missing_fields_error():
    machine_reading = {
        "footfall": 3000000,
        "temp": -19,
        "aqi": 3,
    }
    
    response = requests.post(url, json=machine_reading)
    resp = response.json()

    assert "error_message" in resp
    assert "failure_likelihood" in resp
    assert resp["error_message"] is not None
    assert "Incorrect data sent to predict service." in resp["error_message"]
