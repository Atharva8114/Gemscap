from sqlalchemy import (
    create_engine, Column, Integer, Float, String, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///data/market.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Tick(Base):
    __tablename__ = "ticks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Float)
    timestamp = Column(DateTime, index=True)


class ResampledBar(Base):
    __tablename__ = "resampled_bars"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)  # 1s, 1m, 5m
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    timestamp = Column(DateTime, index=True)


def init_db():
    Base.metadata.create_all(bind=engine)
