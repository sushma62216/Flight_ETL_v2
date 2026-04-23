import streamlit as st
import pydeck as pdk
import pandas as pd
import time
from retrieve_data import load_data_from_db

st.set_page_config(page_title="Flight Tracker", layout="wide")
st.title("✈️ Live Flight Activity Dashboard")

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_data():
    return load_data_from_db()

df = load_data()

if df.empty:
    st.warning("No flight data available.")
    st.stop()

# ── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("Filters")

countries = sorted(df["origin_country"].dropna().unique().tolist())
sources = sorted(df["position_source"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Origin Country", options=countries, default=countries
)
selected_sources = st.sidebar.multiselect(
    "Position Source", options=sources, default=sources
)

auto_refresh = st.sidebar.toggle("Auto-refresh (60s)", value=False)

# ── Apply filters ────────────────────────────────────────────────────────────
filtered_df = df[
    df["origin_country"].isin(selected_countries) &
    df["position_source"].isin(selected_sources)
]

if filtered_df.empty:
    st.warning("No flights match the selected filters.")
    st.stop()
