import requests
from bs4 import BeautifulSoup


class MVVLive(object):
    def __init__(self, stop_name=None, stop_id=None, line=None):
        """Initializes MVVLive object.

        Args:
            stop_name (_type_, optional): Stop name. Will be used to find stop id. To be sure the correct stop is identified, look it up yourself at https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}. Must be provided if stop_id is not provided. Will be ignored if stop_id is provided. Defaults to None.

            stop_id (_type_, optional): Stop ID according to GTFS standard. Look up your stop's ID here: https://www.mvg.de/api/fahrinfo/location/queryWeb?q={stop_name}. Examples are: "de:09162:2" for Marienplatz, "de:09162:6" for Hauptbahnhof, "de:09162:1" for Karlsplatz (Stachus), "de:09184:460" for Garching-Forschungszentrum, etc. Must be provided if stop_name is not provided. Defaults to None.

            line (str): Name of S-Bahn line. Available lines are: "S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20". Defaults to None.
        """
        self.stop_name = stop_name
        self.stop_id = stop_id
        self.line = line
        if self.stop_name is not None or self.stop_id is not None:
            self.update_data()
        if self.line is not None:
            self.update_punctuality()
        self._punctuality = None
        self.data = None

    def update_data(self):
        """Updates data, which is a dictionary of the following format:
        {
            "servingLines": servingLines,
            "departures": departures
        }
        where both servingLines and departures is a list of dicts.

        Raises:
            ValueError: If neither stop_name nor stop_id is provided.
        """
        
        stop_name = self.stop_name
        stop_id = self.stop_id

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
        
        data_response = requests.get(f"https://www.mvg.de/api/fahrinfo/departure/{stop_id}?footway=0")
        self.data = data_response.json()

        return

    def update_punctuality(self):
        """Scrapes punctuality off of S-Bahn line from MVV website
        http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget.

        Raises:
            ValueError: Line not available
            ConnectionError: Error while fetching data from MVV website.
        """

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
            self._punctuality = line_punctuality
            return
        
        # Formatting
        line_punctuality = line_punctuality.replace(" %", "")
        line_punctuality = int(line_punctuality)

        self._punctuality = line_punctuality

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

        if blacklist is not None:
            data = [x for x in data if not any(x[key] in value for key, value in blacklist.items())]
        if whitelist is not None:
            data = [x for x in data if any(x[key] in value for key, value in whitelist.items())]
        
        return data

    @property
    def data(self):
        """Returns the data dict."""
        return self.data

    @property
    def departures(self):
        """Returns a list of departure dicts."""
        return self.data["departures"]

    @property
    def serving_lines(self):
        """Returns a list of serving line dicts."""
        return self.data["servingLines"]
    
    @property
    def punctuality(self):
        """Returns punctuality of S-Bahn line."""
        return self._punctuality

    @data.setter
    def data(self, value):
        """Sets data dict."""
        self._data = value
    
    @punctuality.setter
    def punctuality(self, value):
        """Sets punctuality."""
        self._punctuality = value
