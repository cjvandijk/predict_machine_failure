import requests

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

response = requests.post(url, json=machine_readings)
print(response.json())
