import uvicorn
from fastapi import FastAPI
from service.router import router as car_router


app = FastAPI()
app.include_router(car_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
