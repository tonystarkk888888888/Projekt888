import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SCM Digital Twin", layout="wide")

API_URL = st.secrets["API_URL"]

st.sidebar.title("Controls")
run_sim = st.sidebar.button("Run Simulation")
get_kpi = st.sidebar.button("Get KPIs")
run_forecast = st.sidebar.button("Run Forecast")

st.title("📦 Supply Chain Digital Twin AI")

col1, col2, col3 = st.columns(3)

if get_kpi:
    data = requests.get(f"{API_URL}/kpis").json()
    col1.metric("Service Level", data["service_level"])
    col2.metric("Fill Rate", data["fill_rate"])
    col3.metric("Cost (€)", data["cost"])

if run_sim:
    res = requests.post(f"{API_URL}/simulate").json()
    df = pd.DataFrame({
        "Day": range(1, len(res["inventory"]) + 1),
        "Inventory": res["inventory"],
        "Demand": res["demand"]
    })
    st.subheader("Inventory Simulation")
    st.line_chart(df.set_index("Day"))

if run_forecast:
    res = requests.get(f"{API_URL}/forecast").json()
    hist = pd.DataFrame({"Demand": res["historical"]})
    fore = pd.DataFrame({"Demand": res["forecast"]})
    st.subheader("Demand Forecast")
    st.line_chart(hist)
    st.line_chart(fore)

st.subheader("KPI History")
hist = requests.get(f"{API_URL}/history").json()
if hist:
    st.dataframe(pd.DataFrame(hist))
