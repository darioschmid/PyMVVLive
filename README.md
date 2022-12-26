PyMVVLive
=========

This Python library is designed to fetch data about public transportation in Munich, Germany.
Available data consists of departure and serving line information for every stop in the MVV region, and also punctuality information for S-Bahn lines (S-Bahn München, DB).
The former departure and serving line information is retrieved from MVV's API endpoint at https://www.mvg.de/api/fahrinfo/departure, whereas punctuality information is scraped from this website usind the beautifulsoup package: http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?&statusWidget.


Note that this package only provides **live** data. For information on planned trips and departure information in the middle and distant future, please refer to https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/opendata/index.html.


If you have any idea or further information about how to retrieve S-Bahn punctuality information that does **not** rely on website scraping like it does now (maybe some API), please contact me or contribute to this project.


**Disclaimer**: This project is **not** associated with neither MVV, nor MVG, nor Deutsche Bahn.


MVVLive
=======

## Install it from PyPI
```
pip install MVVLive
```

## Usage

### `MVVLive.get_punctuality()`

Get punctuality information about a certain S-Bahn line. See [below](###example-output-of-`mvvlive.get_punctuality()`) for example output.

```python
import MVVLive
import json

live = MVVLive.MVVLive()

line = "S3"
live.get_punctuality(line)
```

### `MVVLive.get_serving_lines()`

Get information about all the lines served at a certain public transport stop. See [below](###example-output-of-`mvvlive.get_serving_lines()`) for example output.

```python
import MVVLive
import json

live = MVVLive.MVVLive()

stop_id = "de:09184:460"  # stop ID of "Garching Forschungszentrum"
whitelist = {
    "lineNumber": ["U6", "230", "X201"],
}
serving_lines = live.get_serving_lines(stop_name=stop, stop_id=None, whitelist=whitelist, blacklist=None)
```

Both blacklist and whitelist can be provided. The must be a dict in the same format as an element from the `serving_lines` list, except the value must be a list of values (e.g., `"lineNumber": ["U6", "230", "X201"]` instead of `"lineNumber": "U6"`).
You can either provide a `stop_name` or a `stop_id`, where the latter is better as you can ensure the right stop is 
determined. Look it up at https://www.mvg.de/api/fahrinfo/location/queryWeb?q=YOUR_STOP_NAME.

### `MVVLive.get_departures()`

Get information about all departures at a certain public transport stop. See [below](###example-output-of-`mvvlive.get_departures()`) for example output.

```python
import MVVLive
import json

live = MVVLive.MVVLive()

stop = "Höllriegelskreuth"
blacklist = {
    "product": ["REGIONAL_BUS"],
}
departures = live.get_departures(stop_name=stop, stop_id=None, whitelist=None, blacklist=blacklist)
```

Both blacklist and whitelist can be provided. The must be a dict in the same format as an element from the `departures` list, except the value must be a list of values (e.g., `"label": ["U6", "230", "X201"]` instead of `"label": "U6"`).
You can either provide a `stop_name` or a `stop_id`, where the latter is better as you can ensure the right stop is 
determined. Look it up at https://www.mvg.de/api/fahrinfo/location/queryWeb?q=YOUR_STOP_NAME.

## Example Output

### Example Output of `MVVLive.get_punctuality()`

```python
100
```

### Example Output of `MVVLive.get_serving_lines()`

```python
[
    {
        "destination": "Deisenhofen",
        "sev": False,
        "network": "ddb",
        "product": "SBAHN",
        "lineNumber": "S3",
        "divaId": "92M03"
    },
    {
        "destination": "Messestadt Ost",
        "sev": False,
        "network": "swm",
        "product": "UBAHN",
        "lineNumber": "U2",
        "divaId": "010U2"
    },
    {
        "destination": "Sendlinger Tor U",
        "sev": False,
        "network": "swm",
        "product": "TRAM",
        "lineNumber": "17",
        "divaId": "02017"
    },
    {
        "destination": "Ackermannbogen via Münchner Freiheit U",
        "sev": False,
        "network": "swm",
        "product": "BUS",
        "lineNumber": "59",
        "divaId": "03059"
    },
    {
        "destination": "Winning, Riegerweg/Altersheim",
        "sev": False,
        "network": "mvv",
        "product": "REGIONAL_BUS",
        "lineNumber": "220",
        "divaId": "19220"
    }
]
```

### Example Output of `MVVLive.get_departures()`

```python
[
    {
        "departureTime": 1672060500000,
        "product": "TRAM",
        "label": "17",
        "destination": "Sendlinger Tor U",
        "live": False,
        "delay": 0,
        "cancelled": False,
        "lineBackgroundColor": "#ea4029",
        "departureId": "07e4533ca5585437c959fdeb9980e3d1#1672060500000#de:09162:6",
        "sev": False,
        "platform": "",
        "stopPositionNumber": 0,
        "infoMessages": []
    },
    {
        "departureTime": 1672060920000,
        "product": "UBAHN",
        "label": "U2",
        "destination": "Messestadt Ost",
        "live": False,
        "delay": 0,
        "cancelled": False,
        "lineBackgroundColor": "#dd3d4d",
        "departureId": "5c89169b4eac9e688234efa99532f10c#1672060920000#de:09162:6",
        "sev": False,
        "platform": "U2/8 Gleis 2",
        "stopPositionNumber": 0,
        "infoMessages": []
    },
    {
        "departureTime": 1672060980000,
        "product": "SBAHN",
        "label": "S3",
        "destination": "Deisenhofen",
        "live": False,
        "delay": 1,
        "cancelled": False,
        "lineBackgroundColor": "#942d8d",
        "departureId": "0a78778e46079d11830c36fca7566b36#1672060980000#de:09162:6",
        "sev": False,
        "platform": "1",
        "stopPositionNumber": 0,
        "infoMessages": [
            "Linie S3: Maskenpflicht nach gesetzl. Regelung; wir empfehlen eine FFP2-Maske Linie S3: Fahrradmitnahme begrenzt möglich Linie S3: Bei Fahrradmitnahme Sperrzeiten beachten Linie S3: nur 2. Kl."
        ]
    },
    {
        "departureTime": 1672060680000,
        "product": "BUS",
        "label": "59",
        "destination": "Ackermannbogen via Münchner Freiheit U",
        "live": False,
        "delay": 0,
        "cancelled": False,
        "lineBackgroundColor": "#0d5c70",
        "departureId": "0b10f46a89dc6a150f5db24e7ca26f14#1672060680000#de:09162:1110",
        "sev": False,
        "platform": "Pos. 7",
        "stopPositionNumber": 7,
        "infoMessages": []
    },
    {
        "departureTime": 1672061100000,
        "product": "REGIONAL_BUS",
        "label": "220",
        "destination": "Winning, Riegerweg/Altersheim",
        "live": False,
        "delay": 0,
        "cancelled": False,
        "lineBackgroundColor": "#0d5c70",
        "departureId": "14d5f38f4e1169b03e25752dd25259f5#1672061100000#de:09162:1110",
        "sev": False,
        "platform": "Pos. 10",
        "stopPositionNumber": 10,
        "infoMessages": []
    }
]

```



- **line** (*Required*): Name of the S-Bahn line. Can be any of the 8 S-Bahn lines `S1, S2, S3, S4, S6, S7, S8, S20`.

```python
{
    "servingLines": [
        {
            "destination": "Deisenhofen",
            "sev": False,
            "network": "ddb",
            "product": "SBAHN",
            "lineNumber": "S3",
            "divaId": "92M03"
        },
        {
            "destination": "Messestadt Ost",
            "sev": False,
            "network": "swm",
            "product": "UBAHN",
            "lineNumber": "U2",
            "divaId": "010U2"
        },
        {
            "destination": "Sendlinger Tor U",
            "sev": False,
            "network": "swm",
            "product": "TRAM",
            "lineNumber": "17",
            "divaId": "02017"
        },
        {
            "destination": "Ackermannbogen via Münchner Freiheit U",
            "sev": False,
            "network": "swm",
            "product": "BUS",
            "lineNumber": "59",
            "divaId": "03059"
        },
        {
            "destination": "Winning, Riegerweg/Altersheim",
            "sev": False,
            "network": "mvv",
            "product": "REGIONAL_BUS",
            "lineNumber": "220",
            "divaId": "19220"
        }
    ],
    "departures": [
        {
            "departureTime": 1672060500000,
            "product": "TRAM",
            "label": "17",
            "destination": "Sendlinger Tor U",
            "live": False,
            "delay": 0,
            "cancelled": False,
            "lineBackgroundColor": "#ea4029",
            "departureId": "07e4533ca5585437c959fdeb9980e3d1#1672060500000#de:09162:6",
            "sev": False,
            "platform": "",
            "stopPositionNumber": 0,
            "infoMessages": []
        },
        {
            "departureTime": 1672060920000,
            "product": "UBAHN",
            "label": "U2",
            "destination": "Messestadt Ost",
            "live": False,
            "delay": 0,
            "cancelled": False,
            "lineBackgroundColor": "#dd3d4d",
            "departureId": "5c89169b4eac9e688234efa99532f10c#1672060920000#de:09162:6",
            "sev": False,
            "platform": "U2/8 Gleis 2",
            "stopPositionNumber": 0,
            "infoMessages": []
        },
        {
            "departureTime": 1672060980000,
            "product": "SBAHN",
            "label": "S3",
            "destination": "Deisenhofen",
            "live": False,
            "delay": 1,
            "cancelled": False,
            "lineBackgroundColor": "#942d8d",
            "departureId": "0a78778e46079d11830c36fca7566b36#1672060980000#de:09162:6",
            "sev": False,
            "platform": "1",
            "stopPositionNumber": 0,
            "infoMessages": [
                "Linie S3: Maskenpflicht nach gesetzl. Regelung; wir empfehlen eine FFP2-Maske Linie S3: Fahrradmitnahme begrenzt möglich Linie S3: Bei Fahrradmitnahme Sperrzeiten beachten Linie S3: nur 2. Kl."
            ]
        },
        {
            "departureTime": 1672060680000,
            "product": "BUS",
            "label": "59",
            "destination": "Ackermannbogen via Münchner Freiheit U",
            "live": False,
            "delay": 0,
            "cancelled": False,
            "lineBackgroundColor": "#0d5c70",
            "departureId": "0b10f46a89dc6a150f5db24e7ca26f14#1672060680000#de:09162:1110",
            "sev": False,
            "platform": "Pos. 7",
            "stopPositionNumber": 7,
            "infoMessages": []
        },
        {
            "departureTime": 1672061100000,
            "product": "REGIONAL_BUS",
            "label": "220",
            "destination": "Winning, Riegerweg/Altersheim",
            "live": False,
            "delay": 0,
            "cancelled": False,
            "lineBackgroundColor": "#0d5c70",
            "departureId": "14d5f38f4e1169b03e25752dd25259f5#1672061100000#de:09162:1110",
            "sev": False,
            "platform": "Pos. 10",
            "stopPositionNumber": 10,
            "infoMessages": []
        }
    ]
}
```



See https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/opendata/index.html for more information.