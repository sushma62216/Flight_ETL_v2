import requests
import json

def extract():
    api="https://opensky-network.org/api/states/all"
    response=requests.get(api)
    data=response.json()

    # The 'states' key contains the flight data in a list of lists
    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]
    states_data = data.get("states", [])

    return states_data, columns


extract()
