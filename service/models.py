from pydantic import BaseModel
from typing import Union, List


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