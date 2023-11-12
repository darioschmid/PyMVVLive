MVVLive
=======

This Python library is designed to fetch data about public transportation in Munich, Germany.
Available data consists of departure and serving line information for every stop in the MVV region, and also punctuality information for S-Bahn lines (S-Bahn München, DB).
The former departure and serving line information is retrieved from MVV's API endpoint at https://fahrinfo-backend-prod.web.azrapp.swm.de/rest/v2, whereas punctuality information is scraped from this website usind the beautifulsoup package: http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?&statusWidget.


Note that this package only provides **live** data. For information on planned trips and departure information in the middle and distant future, please refer to https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/opendata/index.html.


If you have any idea or further information about how to retrieve S-Bahn punctuality information that does **not** rely on website scraping like it does now (maybe some API), please contact me or contribute to this project.


**Disclaimer**: This project is **not** associated with MVV, MVG, or Deutsche Bahn.


Installation
============

```
pip install MVVLive
```

Usage
=====

See [demo.py](demo.py) for a demo, or see the following documentation.

## `MVVLive.punctuality`

Get punctuality information about a certain S-Bahn line. See [below](#example-output-of-mvvlivepunctuality) for example output.
Update this information by executing `MVVLive.update_punctuality()`.

```python
import MVVLive
API_KEY = 'your_api_key'

# Initialize MVVLive object with line
line = "S3"
live = MVVLive.MVVLive(api_key=API_KEY, line=line)

# Print punctuality
print(live.punctuality)
```

## `MVVLive.departures`

Get information about all departures at a certain public transport stop. See [below](#example-output-of-mvvlivedepartures) for example output.
Update this information by executing `MVVLive.update_departures()`.
You can find out your `stop_id` by executing `MVVLive.get_stops(api_key)`.

```python
import MVVLive
import json
API_KEY = 'your_api_key'

# Initialize MVVLive object with stop id
stop_id = "de:09184:2310"  # stop id of Unterhaching station
live = MVVLive.MVVLive(api_key = API_KEY, stop_id=stop_id)

departures = live.departures

# Print serving lines in a nicely formatted way.
print(json.dumps(departures, indent=4, ensure_ascii=False))
```

Both blacklist and whitelist can be provided. The must be a dict in the same format as an element from the `departures` list, except the value must be a list of values (e.g., `"destination": ["Deisenhofen", "Holzkirchen"]` instead of `"destination": "Deisenhofen"`).

##  `MVVlive.filter()`

Filters data (servingLines or departures) according to a whitelist or blacklist.

```python
import MVVLive
import json
from time import time
API_KEY = 'your_api_key'

# Initialize MVVLive object with stop name
stop_id = "de:09184:2310"
live = MVVLive.MVVLive(api_key=API_KEY, stop_id=stop_id)

# Filter departures
in_30_min = round((time()+30*60)*1000)
blacklist_departures = {
    "destination": ["Deisenhofen", "Holzkirchen"],
}
whitelist_departures = {
    "label": ["S3"],
    "realtimeDepartureTime": range(in_30_min),
}
departures = live.filter(live.departures, whitelist=whitelist_departures, blacklist=blacklist_departures)

# Print serving lines in a nicely formatted way.
print(json.dumps(departures, indent=4, ensure_ascii=False))
```

## `MVVLive.update_punctuality()`

Updates the punctuality information. Gets executed on creation if `line` is provided.

## `MVVLive.update_departures()`

Updates the departures information. Gets executed on creation if `stop_id` is provided.

## Example Output

### Example Output of `MVVLive.punctuality`

```
100
```

### Example Output of `MVVLive.departures`

```json
[
    {
        "plannedDepartureTime": 1699803420000,
        "realtime": true,
        "delayInMinutes": 1,
        "realtimeDepartureTime": 1699803480000,
        "transportType": "SBAHN",
        "label": "S3",
        "divaId": "92M03",
        "network": "ddb",
        "trainType": "",
        "destination": "Mammendorf",
        "cancelled": false,
        "sev": false,
        "platform": 1,
        "messages": [],
        "bannerHash": "",
        "occupancy": "UNKNOWN",
        "stopPointGlobalId": ""
    },
    {
        "plannedDepartureTime": 1699803840000,
        "realtime": true,
        "delayInMinutes": 2,
        "realtimeDepartureTime": 1699803960000,
        "transportType": "SBAHN",
        "label": "S3",
        "divaId": "92M03",
        "network": "ddb",
        "trainType": "",
        "destination": "Deisenhofen",
        "cancelled": false,
        "sev": false,
        "platform": 2,
        "messages": [],
        "bannerHash": "",
        "occupancy": "UNKNOWN",
        "stopPointGlobalId": ""
    },
    ...
]
```
