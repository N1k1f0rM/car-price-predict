from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from .models import ItemResponse, Item
from db.database import get_async_session, Cars, engine, Base
from joblib import load
import pandas as pd
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


router = APIRouter(prefix="/car", tags=["Car"])
model = load('reg.joblib')

def pydantic_to_df(model_instance):
    return pd.DataFrame([jsonable_encoder(model_instance)])


@router.post("/predict", response_model=ItemResponse)
async def predicti(item: Item,
             session: AsyncSession = Depends(get_async_session)) -> dict:

    instance = pydantic_to_df(item)
    prediction = model.predict(instance).tolist()[0]

    response = item.model_dump(by_alias=True)
    response.update({'prediction': prediction})

    try:
        stms = insert(Cars).values(
            year=item.year,
            km_driven=item.km_driven,
            mileage=item.mileage,
            engine=item.engine,
            max_power=item.max_power,
            seats=item.seats,
            price=prediction
        )

        await session.execute(stms)
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return response


@router.get("/my_cars")
async def get_cars(session: AsyncSession = Depends(get_async_session)):

    try:
        link = await session.execute(select(Cars))
        cars = link.scalars().all()
        await session.commit()

        return cars

    except Exception as e:
        raise HTTPException(500, detail=f"{e}")


@router.on_event("shutdown")
async def shutdown_event(session: AsyncSession = Depends(get_async_session)):

    await session.execute(delete(Cars))
    await session.commit()
