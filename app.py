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

# ── KPI row ──────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Flights", len(filtered_df))
col2.metric(
    "Avg Speed (m/s)",
    f"{filtered_df['velocity'].mean():.1f}" if filtered_df['velocity'].notna().any() else "—"
)
col3.metric(
    "Avg Altitude (m)",
    f"{filtered_df['geo_altitude'].mean():.0f}" if filtered_df['geo_altitude'].notna().any() else "—"
)
col4.metric("Countries", filtered_df["origin_country"].nunique())

st.divider()

# ── Charts ───────────────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Top 15 Origin Countries")
    top_countries = (
        filtered_df["origin_country"]
        .value_counts()
        .head(15)
        .rename_axis("country")
        .reset_index(name="flights")
    )
    if top_countries.empty:
        st.info("No country data available for current filters.")
    else:
        st.bar_chart(top_countries.set_index("country"))

with chart_col2:
    st.subheader("Velocity vs Altitude")
    scatter_df = filtered_df[["velocity", "geo_altitude", "position_source"]].dropna()
    if scatter_df.empty:
        st.info("No data available for current filters.")
    else:
        st.scatter_chart(scatter_df, x="velocity", y="geo_altitude", color="position_source")
