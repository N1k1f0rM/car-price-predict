import requests

url = "http://127.0.0.1:8000/predicts"
data = {
    "objects": [
        {
            "year": 2020,
            "km_driven": 15000,
            "mileage": 15.0,
            "engine": 1.5,
            "max_power": 100.0,
            "seats": 5
        },
        {
            "year": 2005,
            "km_driven": 150000,
            "mileage": 30.0,
            "engine": 0.5,
            "max_power": 86.0,
            "seats": 4
        },
        {
            "year": 2023,
            "km_driven": 100,
            "mileage": 1.0,
            "engine": 1000,
            "max_power": 2000.0,
            "seats": 7
        }
    ]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Predictions:", response.json())
else:
    print("Error:", response.status_code, response.text)