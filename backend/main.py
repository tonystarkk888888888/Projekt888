from fastapi import FastAPI
import random
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SCM Digital Twin API running"}

@app.post("/simulate")
def simulate():
    days = 30
    inventory = 100
    demand_data = []
    inventory_levels = []

    for day in range(days):
        demand = random.randint(5, 20)
        inventory -= demand

        if inventory < 20:
            inventory += 50

        demand_data.append(demand)
        inventory_levels.append(inventory)

    return {"demand": demand_data, "inventory": inventory_levels}

@app.get("/kpis")
def kpis():
    return {
        "service_level": round(random.uniform(0.85, 0.99), 2),
        "fill_rate": round(random.uniform(0.80, 0.95), 2),
        "cost": random.randint(1000, 5000)
    }

@app.get("/forecast")
def forecast():
    days = 30
    demand = np.array([random.randint(5, 20) for _ in range(days)])

    X = np.arange(days).reshape(-1, 1)
    model = LinearRegression().fit(X, demand)

    future = np.arange(days, days + 10).reshape(-1, 1)
    forecast = model.predict(future)

    return {
        "historical": demand.tolist(),
        "forecast": forecast.tolist()
    }
