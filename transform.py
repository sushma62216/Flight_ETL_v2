from extract import extract
import pandas as pd


def transformed_data(ti,** kwargs):
    states_data, columns = ti.xcom_pull(task_ids="extracting_data")

    if not states_data:
        raise ValueError("No flight data received from extract task")
    
    df=pd.DataFrame(states_data,columns=columns)

    df.rename(columns={"icao24": "aircraft_id","callsign": "flight_number"}, inplace=True)

    df['time_position']=pd.to_datetime(df['time_position'],unit='s',utc=True)
    df['time_position']=df['time_position']-pd.Timedelta(hours=5)
    df['time_position']=df['time_position'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S')if pd.notnull(x) else None)

    df['time_position'] = pd.to_datetime(df['time_position'], errors='coerce')
    df['time']=df['time_position'].dt.time
    df['date']=df['time_position'].dt.date

    dropped_columns=['time_position','last_contact','baro_altitude','on_ground','true_track','sensors','squawk','spi']
    df=df.drop(dropped_columns,axis=1)

    df = df.dropna(subset=["time", "date"])

    df['longitude']=round(df['longitude'],2)
    df['latitude']=round(df['latitude'],2)

    position_source_mapping={0:'ADS-B',1:'ASTERIX',2:'MLAT',3:'FLARM'}
    df['position_source']=df['position_source'].map(position_source_mapping)

    
    ti.xcom_push(key="df_json", value=df.to_json(orient="records"))
    return df

