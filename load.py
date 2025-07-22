import psycopg2
from db_config import DB_CONFIG
import pandas as pd
from db_schema import create_tables

def load_to_db(ti,**context):
    json_data = ti.xcom_pull(key='df_json', task_ids='transforming_data')

    if json_data is None:
        print("No data received from XCom. after transformation")

    df = pd.read_json(json_data, orient='records')
    print("Data to load:")
    print(df.head())
    
    conn=psycopg2.connect(**DB_CONFIG)
    cursor=conn.cursor()

    cursor.execute("SELECT inet_server_addr(), current_database(), current_user;")
    print("Airflow DB Connection:", cursor.fetchone())

    
    create_tables()
    
    #aircraft table
    aircraft_rows=df[['aircraft_id','origin_country']].drop_duplicates()
    for row in aircraft_rows.itertuples(index=False):
        cursor.execute("""INSERT INTO aircraft(aircraft_id,origin_country) 
                        VALUES(%s,%s)
                       ON CONFLICT (aircraft_id) DO NOTHING;""",row)
        
    #flight_status table
    flight_status_rows=df[['aircraft_id','flight_number','position_source','time','date']].drop_duplicates()
    for row in flight_status_rows.itertuples(index=False):
        cursor.execute("""INSERT INTO flight_status(aircraft_id,flight_number,position_source,time,date) 
                        VALUES(%s,%s,%s,%s,%s)""",row)
        
    #flight_position table
    flight_position_rows=df[['aircraft_id','longitude','latitude','velocity','vertical_rate','geo_altitude','time','date']].drop_duplicates()
    for row in flight_position_rows.itertuples(index=False):
        cursor.execute("""INSERT INTO flight_position(aircraft_id,longitude,latitude,velocity,vertical_rate,geo_altitude,time,date) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",row)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data Loaded successfully !")