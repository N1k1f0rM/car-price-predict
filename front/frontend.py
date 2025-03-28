import pandas as pd
import streamlit as st
from datetime import datetime
import asyncio
import httpx
import json


st.title("Car price prediction")

st.header("Input info about car")

year = st.number_input("Год выпуска", min_value=1800, max_value=datetime.now().year)
km_driven = st.number_input("Пробег (км)", min_value=0)
mileage = st.number_input("Расход топлива (км/л):", min_value=0.0, value=15.0)
engine = st.number_input("Объем двигателя (см³):", min_value=0, value=1500)
max_power = st.number_input("Максимальная мощность (л.с.):", min_value=0.0, value=100.0)
seats = st.number_input("Количество мест:", min_value=1, max_value=10, value=5)

data_to_post = {
        "year": int(year),
        "km_driven": int(km_driven),
        "mileage": float(mileage),
        "engine": int(engine),
        "max_power": float(max_power),
        "seats": int(seats)
}


async def make_pred(data):

    try:
        async with httpx.AsyncClient() as client:
           r = await client.post("http://0.0.0.0:8000/car/predict", json=data)
           return r.json()

    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {e}"}  # Обработка ошибок HTTP
    except httpx.RequestError as e:
        return {"error": f"Request Error: {e}"}  # Обработка ошибок подключения/запроса
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from the API"}


if st.button("Show price"):
    result = asyncio.run(make_pred(data_to_post))

    if "error" in result:
        st.error(result)
    else:
        st.success(f"Your price: {round(int(result['prediction']), 2)}₽")


st.header("Get my cars list")


async def get_my_cats():

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8000/car/my_cars")

            if resp.status_code == 200:
                cars_data = resp.json()
                cars_table = pd.DataFrame(cars_data)
            else:
                st.error(f"Ошибка при получении данных: {resp.status_code} - {resp.text}")

        return cars_table
    except Exception as e:
        st.error(f"Ошибка подключения к API: {e}")


if st.button("Show my cars"):
    result = asyncio.run(get_my_cats())
    st.success(st.dataframe(result))
