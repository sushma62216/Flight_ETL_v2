import streamlit as st
from retrieve_data import load_data_from_db

st.set_page_config(page_title="Flight Tracker", layout="wide")
st.title("✈️ Live Flight Activity Dashboard")

df = load_data_from_db()

if df.empty:
    st.warning("No flight data available.")
else:
    st.metric("Total Flights Tracked", len(df))

    st.subheader("Flights by Origin Country")
    st.bar_chart(df["origin_country"].value_counts())

    st.subheader("Flight Data Table")
    st.dataframe(df)
