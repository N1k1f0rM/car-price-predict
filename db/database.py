from sqlalchemy import Integer, Float, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from datetime import datetime
from config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class Cars(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    time: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    km_driven: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[float] = mapped_column(Float, nullable=False)
    engine: Mapped[int] = mapped_column(Integer, nullable=False)
    max_power: Mapped[float] = mapped_column(Float, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)


engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with session() as ses:
        yield ses
