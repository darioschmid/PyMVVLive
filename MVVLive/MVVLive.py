import requests
from bs4 import BeautifulSoup


class MVVLive(object):
    def __init__(self):
        pass

    def get_punctuality(self, line):
        """Scrapes punctuality off of S-Bahn line from MVV website
        http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget.

        Args:
            line (str): Name of S-Bahn line. Available lines are: "S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20".

        Raises:
            ValueError: Line not available
            ConnectionError: Error while fetching data from MVV website.

        Returns:
            _type_: punctuality of line from "0" to "100" (or "-" if no data is available in case of S20).
        """

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
            raise ConnectionError(
                f"Error while fetching data from MVV website. Status code: {response.status_code}"
            )

        # Parse BeautifulSoup HTML-document from source code
        soup = BeautifulSoup(response.text, "html.parser")

        # Find row with our line
        line_row = soup.find("tr", id=f"select_S {line_number}")
        line_columns = line_row.find_all("td")
        line_punctuality = line_columns[2].text

        if line_punctuality == "-":
            return line_punctuality
        
        # Formatting
        line_punctuality = line_punctuality.replace(" %", "")
        line_punctuality = int(line_punctuality)

        return line_punctuality

    def get_data(self, stop_name=None, stop_id=None):
        """Returns a dictionary of the following format:
        {
            "servingLines": servingLines,
            "departures": departures
        }
        where both servingLines and departures is a list of dicts.

        Args:
            stop_name (str, optional): Stop name. Will be used to find stop id. To be sure the correct stop is identified,
                                       look it up yourself at https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}.
                                       Defaults to None. Must be provided if stop_id is not provided.
            stop_id (str, optional): Stop ID according to GTFS standard.
                                     Look up your stop's ID here: https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}.
                                     Examples are: "de:09162:2" for Marienplatz, "de:09162:6" for Hauptbahnhof,
                                     "de:09162:1" for Karlsplatz (Stachus), "de:09184:460" for Garching-Forschungszentrum, etc.
                                     Defaults to None. Must be provided if stop_name is not provided.

        Raises:
            ValueError: If neither stop_name nor stop_id is provided.

        Returns:
            list: list of departure dicts.
        """

        if stop_name is None and stop_id is None:
            raise ValueError("Either stop_name or stop_id must be provided.")

        if stop_id is None:
            # stop ID not provided, get it from stop name
            stop_response = requests.get(f"https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}", timeout=20)
            # exit if response is not 200
            if stop_response.status_code != 200:
                raise ConnectionError(
                    f"Error while fetching data from MVV website. Status code: {stop_response.status_code}"
                )
            stop_id = stop_response.json()['locations'][0]['id']
            #print(f"stop ID: {stop_id}")
        
        departures_response = requests.get(f"https://www.mvg.de/api/fahrinfo/departure/{stop_id}?footway=0")
        departures = departures_response.json()

        return departures
    
    def filter_departures(self, departures, whitelist=None, blacklist=None):
        """Filters a list of departures according to a whitelist or blacklist.

        Args:
            departures (list): List of departure dicts.
            whitelist (dict, optional): Whitelist dict according to which will be filtered. Its values need to be lists.
                                        See README.md for more details. Defaults to None.
            blacklist (dict, optional): Blacklist dict according to which will be filtered. Its values need to be lists.
                                        See README.md for more details. Defaults to None.
        Returns:
            _type_: Returns a filtered list departures.
        """

        if blacklist is not None:
            filtered_departues = [departure for departure in departures if not any(departure[key] in value for key, value in blacklist.items())]
        if whitelist is not None:
            filtered_departues = [departure for departure in departures if any(departure[key] in value for key, value in whitelist.items())]
        if blacklist is None and whitelist is None:
            filtered_departues = departures
        
        return filtered_departues
