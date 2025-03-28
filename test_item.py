import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "year": 2020,
    "km_driven": 15000,
    "mileage": 15.0,
    "engine": 1.5,
    "max_power": 100.0,
    "seats": 5
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Prediction:", response.json())
else:
    print("Error:", response.status_code, response.text)