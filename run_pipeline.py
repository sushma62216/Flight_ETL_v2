"""Standalone ETL runner — bypasses Airflow XCom for local execution."""
import requests
import json
import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "opensky",
    "user": "postgres",
    "password": "Sushma@2025",
}

# ── Extract ───────────────────────────────────────────────────────────────────
print("Extracting...")
response = requests.get("https://opensky-network.org/api/states/all", timeout=15)
if response.status_code != 200:
    raise ValueError(f"OpenSky API returned {response.status_code}")
data = response.json()
columns = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
    "spi", "position_source"
]
states_data = data.get("states", [])
print(f"  {len(states_data)} flights received")

# ── Transform ─────────────────────────────────────────────────────────────────
print("Transforming...")
df = pd.DataFrame(states_data, columns=columns)
df.rename(columns={"icao24": "aircraft_id", "callsign": "flight_number"}, inplace=True)

df['time_position'] = pd.to_datetime(df['time_position'], unit='s', utc=True)
df['time_position'] = df['time_position'] - pd.Timedelta(hours=5)
df['time_position'] = df['time_position'].apply(
    lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None)
df['time_position'] = pd.to_datetime(df['time_position'], errors='coerce')
df['time'] = df['time_position'].dt.time
df['date'] = df['time_position'].dt.date

dropped = ['time_position', 'last_contact', 'baro_altitude', 'on_ground',
           'true_track', 'sensors', 'squawk', 'spi']
df = df.drop(dropped, axis=1).dropna(subset=["time", "date"])

df['longitude'] = round(df['longitude'], 2)
df['latitude'] = round(df['latitude'], 2)
df['position_source'] = df['position_source'].map(
    {0: 'ADS-B', 1: 'ASTERIX', 2: 'MLAT', 3: 'FLARM'})
print(f"  {len(df)} rows after cleaning")

# ── Load ──────────────────────────────────────────────────────────────────────
print("Loading into PostgreSQL...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS aircraft (
    aircraft_id TEXT PRIMARY KEY,
    origin_country TEXT
);""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS flight_status (
    id SERIAL PRIMARY KEY,
    aircraft_id TEXT REFERENCES aircraft(aircraft_id),
    flight_number TEXT,
    position_source TEXT,
    time TIME,
    date DATE
);""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS flight_position (
    id SERIAL PRIMARY KEY,
    aircraft_id TEXT REFERENCES aircraft(aircraft_id),
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    vertical_rate DOUBLE PRECISION,
    geo_altitude DOUBLE PRECISION,
    time TIME,
    date DATE
);""")

for row in df[['aircraft_id', 'origin_country']].drop_duplicates().itertuples(index=False):
    cursor.execute(
        "INSERT INTO aircraft(aircraft_id, origin_country) VALUES(%s,%s) ON CONFLICT DO NOTHING;", row)

for row in df[['aircraft_id', 'flight_number', 'position_source', 'time', 'date']].drop_duplicates().itertuples(index=False):
    cursor.execute(
        "INSERT INTO flight_status(aircraft_id, flight_number, position_source, time, date) VALUES(%s,%s,%s,%s,%s)", row)

for row in df[['aircraft_id', 'longitude', 'latitude', 'velocity', 'vertical_rate', 'geo_altitude', 'time', 'date']].drop_duplicates().itertuples(index=False):
    cursor.execute(
        "INSERT INTO flight_position(aircraft_id, longitude, latitude, velocity, vertical_rate, geo_altitude, time, date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", row)

conn.commit()
cursor.close()
conn.close()
print("Done! Data loaded successfully.")
