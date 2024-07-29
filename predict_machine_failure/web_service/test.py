import requests
import json

machine_readings = {
    "footfall": 83,
    "temp_mode": 4,
    "air_quality": 3, 
    "proximity_sensor": 4, 
    "current_usage": 5, 
    "voc_level": 1, 
    "revolutions_per_minute": 28, 
    "input_pressure": 6,
    "temperature": 1
}

url = 'http://localhost:9696/predict'
req_string = json.dumps(machine_readings)
print(type(req_string), len(req_string), json.loads(req_string))
response = requests.post(url, json=json.dumps(machine_readings))
print("RESPONSE = ", response.json())
