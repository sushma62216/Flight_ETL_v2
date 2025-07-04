import psycopg2
from db_config import DB_CONFIG

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aircraft (
        aircraft_id TEXT PRIMARY KEY,
        origin_country TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flight_status (
        id SERIAL PRIMARY KEY,
        aircraft_id TEXT REFERENCES aircraft(aircraft_id),
        flight_number TEXT,
        position_source TEXT,
        time TIME,
        date DATE
    );
    """)

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
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")
