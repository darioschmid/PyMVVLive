import requests
from bs4 import BeautifulSoup


def punctuality(line):
    """Scrape punctuality of S-Bahn from MVV website"""

    # Check if line is available
    available_lines = ["S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20"]
    if line not in available_lines:
        raise ValueError(
            f"Line {line} not available. Available lines are: {available_lines}"
        )

    #
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
