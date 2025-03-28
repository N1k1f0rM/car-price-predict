from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import List, Union
from joblib import load
import pandas as pd


app = FastAPI()
model = load('reg.joblib')


class Check(BaseModel):
    resp: str


class Item(BaseModel):
    year: int
    km_driven: int
    mileage: Union[float, int]
    engine: Union[float, int]
    max_power: Union[float, int]
    seats: int


class Items(BaseModel):
    objects: List[Item]


class ItemResponse(BaseModel):
    prediction: float


class ItemsResponse(BaseModel):
    predictions: List[dict]


def pydantic_to_df(model_instance):
    return pd.DataFrame([jsonable_encoder(model_instance)])


@app.get("/", response_model=Check)
def check():
    return Check(resp="Api started")


@app.post("/predict", response_model=ItemResponse)
def predicti(item: Item) -> dict:

    instance = pydantic_to_df(item)
    prediction = model.predict(instance).tolist()[0]

    response = item.model_dump(by_alias=True)
    response.update({'prediction': prediction})

    return response


@app.post("/predicts", response_model=ItemsResponse)
def predictis(items: Items) -> ItemsResponse:
    preds = []

    for i in items.objects:
        instance = pydantic_to_df(i)
        prediction = model.predict(instance).tolist()[0]

        response = {
            'year': i.year,
            'km_driven': i.km_driven,
            'mileage': i.mileage,
            'engine': i.engine,
            'max_power': i.max_power,
            'seats': i.seats,
            'prediction': prediction
        }
        preds.append(response)

    return ItemsResponse(predictions=preds)
