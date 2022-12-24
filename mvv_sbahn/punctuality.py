import requests
from bs4 import BeautifulSoup

def punctuality(line):
    """Scrape punctuality of S-Bahn from MVV website"""

    # Check if line is available
    available_lines = ["S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20"]
    if line not in available_lines:
        raise ValueError(f"Line {line} not available. Available lines are: {available_lines}")

    # 
    line_number = line[1:]

    url = "http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?statusWidget"
    response = requests.get(url)

    # Parse BeautifulSoup HTML-document from source code
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find main table
    table = soup.find('table', style="width:100%", cellspacing="0")

    # Find row with our line
    line_row = soup.find('tr', id=f"select_S {line_number}")
    #print(f"{line_row=}")
    # Find columns in line row
    line_columns = line_row.find_all('td')
    #print(f"{line_columns=}")
    # Select punctuality column
    line_punctuality = line_columns[2].text
    #print(f"{line_punctuality=}")
    line_punctuality = line_punctuality.replace(" %", "")

    return line_punctuality
