import json
import requests


def get_departures(station_name, station_id=None, destination_blacklist=None, destination_whitelist=None):
    """Returns a list of departures from a station."""

    if station_id is None:
        # Station ID not provided, get it from station name
        station_response = requests.get(f"https://www.mvg.de/api/fahrinfo/location/queryWeb?q={station_name}")
        # exit if response is not 200
        if station_response.status_code != 200:
            print(f"Error: {station_response.status_code}")
            exit(1)
        station_id = station_response.json()['locations'][0]['id']
        #print(f"Station ID: {station_id}")
    
    departures_response = requests.get(f"https://www.mvg.de/api/fahrinfo/departure/{station_id}?footway=0")
    departures = departures_response.json()['departures']

    # Filter departures
    departures = [destination for destination in departures if destination["product"] == "SBAHN"]  # Filter for S-Bahn
    if destination_blacklist is not None:  
        departures = [x for x in departures if x["destination"] not in destination_blacklist]  # Filter according to blacklist
    if destination_whitelist is not None:  # Filter according to blacklist
        departures = [x for x in departures if x["destination"] in destination_whitelist]

    return departures


if __name__ == "__main__":
    departures = get_departures("Unterhaching", destination_blacklist=["Holzkirchen"])
    print(json.dumps(departures, indent=4, sort_keys=True))