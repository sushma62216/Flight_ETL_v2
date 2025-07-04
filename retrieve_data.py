import psycopg2
import pandas as pd
from db_config import DB_CONFIG

def load_data_from_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT 
                a.aircraft_id,
                a.origin_country,
                s.flight_number,
                s.position_source,
                s.time,
                s.date,
                p.longitude,
                p.latitude,
                p.velocity,
                p.geo_altitude,
                p.vertical_rate
            FROM flight_status s
            JOIN aircraft a ON s.aircraft_id = a.aircraft_id
            JOIN flight_position p ON p.aircraft_id = a.aircraft_id AND p.time = s.time AND p.date = s.date
            ORDER BY s.date DESC, s.time DESC
            LIMIT 100;
        """


        df = pd.read_sql_query(query, conn)

        conn.close()
        return df

    except Exception as e:
        print("Error loading data:", e)
        return pd.DataFrame()
