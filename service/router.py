from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from .models import ItemResponse, ItemsResponse, Items, Item
from joblib import load
import pandas as pd


router = APIRouter(prefix="/car", tags=["Car"])
model = load('reg.joblib')

def pydantic_to_df(model_instance):
    return pd.DataFrame([jsonable_encoder(model_instance)])


@router.post("/predict", response_model=ItemResponse)
def predicti(item: Item) -> dict:

    instance = pydantic_to_df(item)
    prediction = model.predict(instance).tolist()[0]

    response = item.model_dump(by_alias=True)
    response.update({'prediction': prediction})

    return response


@router.post("/predicts", response_model=ItemsResponse)
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