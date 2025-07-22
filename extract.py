import requests
import json

def extract():
    api = "https://opensky-network.org/api/states/all"
    response = requests.get(api, timeout=10)


    if response.status_code != 200:
        raise ValueError(f"OpenSky API returned {response.status_code}")
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON received from OpenSky API")


    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]
    states_data = data.get("states", [])

    return states_data, columns


