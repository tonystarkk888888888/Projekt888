import streamlit as st
import requests
import pandas as pd

st.title("📦 SCM Digital Twin AI")

API_URL = st.secrets["API_URL"]

# --- Simulation ---
if st.button("Run Simulation"):
    res = requests.post(f"{API_URL}/simulate").json()

    df = pd.DataFrame({
        "Day": list(range(1, len(res["inventory"]) + 1)),
        "Inventory": res["inventory"],
        "Demand": res["demand"]
    })

    st.line_chart(df.set_index("Day"))

# --- KPIs ---
if st.button("Get KPIs"):
    kpi = requests.get(f"{API_URL}/kpis").json()

    st.metric("Service Level", kpi["service_level"])
    st.metric("Fill Rate", kpi["fill_rate"])
    st.metric("Cost", kpi["cost"])

# --- Forecast ---
st.subheader("📈 Demand Forecast")

if st.button("Run Forecast"):
    res = requests.get(f"{API_URL}/forecast").json()

    hist = pd.DataFrame({"Demand": res["historical"]})
    fore = pd.DataFrame({"Demand": res["forecast"]})

    st.line_chart(hist)
    st.line_chart(fore)
