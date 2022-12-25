import requests
from bs4 import BeautifulSoup


class MVVsBahn(object):
    def __init__(self):
        pass

    def get_punctuality(self, line):
        """Scrape punctuality of S-Bahn from MVV website"""

        # Check if line is available
        available_lines = ["S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20"]
        if line not in available_lines:
            raise ValueError(
                f"Line {line} not available. Available lines are: {available_lines}"
            )

        line_number = line[1:]

        url = "http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget"
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            raise ValueError(
                f"Error while fetching data from MVV website. Status code: {response.status_code}"
            )

        # Parse BeautifulSoup HTML-document from source code
        soup = BeautifulSoup(response.text, "html.parser")

        # Find row with our line
        line_row = soup.find("tr", id=f"select_S {line_number}")
        line_columns = line_row.find_all("td")
        line_punctuality = line_columns[2].text
        line_punctuality = line_punctuality.replace(" %", "")

        return line_punctuality

    def get_departures(self, station_name, station_id=None, destination_blacklist=None, destination_whitelist=None):
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
