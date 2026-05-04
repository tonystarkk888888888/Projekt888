from fastapi import FastAPI
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class KPI(Base):
    __tablename__ = "kpi_results"
    id = Column(Integer, primary_key=True, index=True)
    service_level = Column(Float)
    fill_rate = Column(Float)
    cost = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API running with PostgreSQL 🚀"}

@app.post("/simulate")
def simulate():
    days = 30
    inventory = 100
    demand_data = []
    inventory_levels = []

    for _ in range(days):
        demand = random.randint(5, 20)
        inventory -= demand
        if inventory < 20:
            inventory += 50
        demand_data.append(demand)
        inventory_levels.append(inventory)

    return {"demand": demand_data, "inventory": inventory_levels}

@app.get("/kpis")
def kpis():
    db = SessionLocal()
    data = {
        "service_level": round(random.uniform(0.85, 0.99), 2),
        "fill_rate": round(random.uniform(0.80, 0.95), 2),
        "cost": random.randint(1000, 5000)
    }
    record = KPI(**data)
    db.add(record)
    db.commit()
    return data

@app.get("/history")
def history():
    db = SessionLocal()
    records = db.query(KPI).all()
    return [{"service_level": r.service_level, "fill_rate": r.fill_rate, "cost": r.cost} for r in records]

@app.get("/forecast")
def forecast():
    days = 30
    demand = np.array([random.randint(5, 20) for _ in range(days)])
    X = np.arange(days).reshape(-1, 1)
    model = LinearRegression().fit(X, demand)
    future = np.arange(days, days + 10).reshape(-1, 1)
    forecast = model.predict(future)
    return {"historical": demand.tolist(), "forecast": forecast.tolist()}
