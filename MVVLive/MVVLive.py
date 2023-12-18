import requests
from bs4 import BeautifulSoup

STATION_URL = """https://fahrinfo-backend-prod.web.azrapp.swm.de/rest/v2/station"""
DEPARTURE_URL = """https://fahrinfo-backend-prod.web.azrapp.swm.de/rest/v2/departure"""
PUNCTUALITY_URL = "http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget"
MESSAGE_URL = """https://fahrinfo-backend-prod.web.azrapp.swm.de/rest/v2/message"""


def get_stops(api_key: str, timeout: int = 20):
    """Return a dictionary of all stops and their available information. Use
        this function to determine the id of your stop of interest.

    :return: Dict of all available stops.
    """

    headers = {'api_key': api_key}
    response = requests.get(STATION_URL, headers=headers, timeout=timeout)
    if response.status_code != 200:
        raise ConnectionError(
            f"Error while fetching data from MVV website. Status code: {response.status_code}"
        )

    return response.json()


class MVVLive:
    def __init__(self, api_key: str = None, stop_id: str = None,
                 line: str = None, timeout: int = 20):
        """Initializes MVVLive object.

        :param stop_id (str, optional): Stop ID according to GTFS standard.
            Look up your stop's ID here:
            https://fahrinfo-backend-prod.web.azrapp.swm.de/rest/v2/station.
            Examples are: "de:09162:2" for Marienplatz, "de:09162:6" for
            Hauptbahnhof, "de:09162:1" for Karlsplatz (Stachus), "de:09184:460"
            for Garching-Forschungszentrum, etc. Must be provided if stop_name
            is not provided. Defaults to None.
        :param line (str): Name of S-Bahn line. Available lines are: "S1",
            "S2", "S3", "S4", "S6", "S7", "S8", "S20". Defaults to None.
        """

        # Set timeout
        self.timeout = timeout

        # Set stop ID. Get it from stop name if not provided.
        self.stop_id = stop_id

        # Set line.
        self.line = line

        # Set API key.
        self.api_key = api_key

        # Update data and punctuality information.
        if self.stop_id:
            self.update_departures()
        if self.line:
            self.update_punctuality()

        self.update_messages()

    def update_departures(self):
        """Updates list of departures.

        Raises:
            ValueError: If neither stop_name nor stop_id is provided.
            ConnectionError: Error while fetching data from MVV API.
        """

        if self.stop_id is None:
            raise ValueError('stop_id is not provided!')

        headers = {'api_key': self.api_key}
        params = {'globalId': self.stop_id}
        data_response = requests.get(DEPARTURE_URL, headers=headers,
                                     params=params, timeout=self.timeout)
        if data_response.status_code != 200:
            raise ConnectionError(
                f"Error while fetching data from MVV API. Status code: {data_response.status_code}"
            )
        self.departures = data_response.json()

        return

    def update_punctuality(self):
        """Scrapes punctuality off of S-Bahn line from MVV website
        http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget.

        Raises:
            ValueError: Line not available
            ConnectionError: Error while fetching data from MVV website.
        """

        if self.line is None:
            raise ValueError('line is not provided!')

        line = self.line

        # Check if line is available
        available_lines = ["S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20"]
        if line not in available_lines:
            raise ValueError(
                f"Line {line} not available. Available lines are: {available_lines}"
            )

        line_number = line[1:]

        response = requests.get(PUNCTUALITY_URL, timeout=self.timeout)
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

    def update_messages(self):

        headers = {'api_key': self.api_key}
        data_response = requests.get(MESSAGE_URL, headers=headers,
                                     timeout=self.timeout)
        if data_response.status_code != 200:
            raise ConnectionError(
                f"Error while fetching data from MVV API. Status code: {data_response.status_code}"
            )
        self.messages = data_response.json()

        return


    def filter(self, data, whitelist=None, blacklist=None):
        """Filters data (servingLines or departures) according to a whitelist
            or blacklist.

        Args:
            data (list): List of data dicts, e.g. departures.
            whitelist (dict, optional): Whitelist dict according to which will
                be filtered. Its values need to be lists. See README.md for
                more details. Defaults to None.
            blacklist (dict, optional): Blacklist dict according to which will
                be filtered. Its values need to be lists. See README.md for
                more details. Defaults to None.
        Returns:
            dict: Returns filtered list data.
        """

        filtered_data = data
        if blacklist is not None:
            filtered_data = [x for x in filtered_data if not any(
                x[key] in value for key, value in blacklist.items())]
        if whitelist is not None:
            filtered_data = [x for x in filtered_data if all(
                x[key] in value for key, value in whitelist.items())]

        return filtered_data
