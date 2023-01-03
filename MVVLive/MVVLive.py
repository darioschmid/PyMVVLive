import requests
from bs4 import BeautifulSoup


class MVVLive:
    def __init__(self, stop_name=None, stop_id=None, line=None):
        """Initializes MVVLive object.

        Args:
            stop_name (str, optional): Stop name. Will be used to find stop id. To be sure the correct stop is identified, look it up yourself at https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}. Must be provided if stop_id is not provided. Will be ignored if stop_id is provided. Defaults to None.

            stop_id (str, optional): Stop ID according to GTFS standard. Look up your stop's ID here: https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}. Examples are: "de:09162:2" for Marienplatz, "de:09162:6" for Hauptbahnhof, "de:09162:1" for Karlsplatz (Stachus), "de:09184:460" for Garching-Forschungszentrum, etc. Must be provided if stop_name is not provided. Defaults to None.

            line (str): Name of S-Bahn line. Available lines are: "S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20". Defaults to None.
        """

        # Set stop ID. Get it from stop name if not provided.
        self.stop_id = stop_id
        if self.stop_id is None:
            if stop_name is not None:
                self.stop_id = self.determine_stop_id(stop_name)

        # Set line.
        self.line = line

        # Update data and punctuality information.
        self.update_data()
        self.update_punctuality()
    
    def determine_stop_id(self, stop_name):
        """Determines stop ID from stop name.

        Returns:
            str: Stop ID.
        """
        stop_response = requests.get(f"https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}")
        if stop_response.status_code != 200:
            raise ConnectionError(
                f"Error while fetching data from MVV website. Status code: {stop_response.status_code}"
            )
        stop_id = stop_response.json()['locations'][0]['id']
        return stop_id

    def update_data(self):
        """Updates data, which is a dictionary of the following format:
        {
            "servingLines": servingLines,
            "departures": departures
        }
        where both servingLines and departures is a list of dicts.

        Raises:
            ValueError: If neither stop_name nor stop_id is provided.
            ConnectionError: Error while fetching data from MVV API.
        """

        if self.stop_id is None:
            #self.data = None
            return
        
        data_response = requests.get(f"https://www.mvg.de/api/fahrinfo/departure/{self.stop_id}?footway=0")
        if data_response.status_code != 200:
            raise ConnectionError(
                f"Error while fetching data from MVV website. Status code: {data_response.status_code}"
            )
        self.data = data_response.json()

        return

    def update_serving_lines(self):
        self.update_data()
        return
    
    def update_departures(self):
        self.update_data()
        return

    def update_punctuality(self):
        """Scrapes punctuality off of S-Bahn line from MVV website
        http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget.

        Raises:
            ValueError: Line not available
            ConnectionError: Error while fetching data from MVV website.
        """

        if self.line is None:
            #self.punctuality = None
            return

        line = self.line

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
            self.punctuality = line_punctuality
            return
        
        # Formatting
        line_punctuality = line_punctuality.replace(" %", "")
        line_punctuality = int(line_punctuality)

        self.punctuality = line_punctuality

        return
  
    def filter(self, data, whitelist=None, blacklist=None):
        """Filters data (servingLines or departures) according to a whitelist or blacklist.

        Args:
            data (list): List of data dicts, e.g. departures.
            whitelist (dict, optional): Whitelist dict according to which will be filtered. Its values need to be lists.
                                        See README.md for more details. Defaults to None.
            blacklist (dict, optional): Blacklist dict according to which will be filtered. Its values need to be lists.
                                        See README.md for more details. Defaults to None.
        Returns:
            dict: Returns filtered list data.
        """

        filtered_data = data
        if blacklist is not None:
            filtered_data = [x for x in filtered_data if not any(x[key] in value for key, value in blacklist.items())]
        if whitelist is not None:
            filtered_data = [x for x in filtered_data if all(x[key] in value for key, value in whitelist.items())]
        
        return filtered_data

    @property
    def departures(self):
        """Returns a list of departure dicts."""
        return self.data["departures"]

    @property
    def serving_lines(self):
        """Returns a list of serving line dicts."""
        return self.data["servingLines"]
