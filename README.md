MVVLive
=========

Python-Library to get punctuality information for S-Bahns in munich from hafas.de. Relies on scraping a website due to the lack of official API in this specific case.
This project *not* associated with neither MVV, MVG, Deutsche Bahn, etc.


## MVVLive.get_punctuality(line)
Retrieve the next departures from http://s-bahn-muenchen.hafas.de/bin/540/query.exe/dn?&statusWidget.

Configuration variables:
 
- **line** (*Required*): Name of the S-Bahn line. Can be any of the 8 S-Bahn lines `S1, S2, S3, S4, S6, S7, S8, S20`.


```yaml
{
    "servingLines": [
        {
            "destination": "Deisenhofen",
            "sev": false,
            "network": "ddb",
            "product": "SBAHN",
            "lineNumber": "S3",
            "divaId": "92M03"
        },
		...
        {
            "destination": "Messestadt Ost",
            "sev": false,
            "network": "swm",
            "product": "UBAHN",
            "lineNumber": "U2",
            "divaId": "010U2"
        },
		...
        {
            "destination": "Sendlinger Tor U",
            "sev": false,
            "network": "swm",
            "product": "TRAM",
            "lineNumber": "17",
            "divaId": "02017"
        },
		...
        {
            "destination": "Ackermannbogen via Münchner Freiheit U",
            "sev": false,
            "network": "swm",
            "product": "BUS",
            "lineNumber": "59",
            "divaId": "03059"
        },
		...
        {
            "destination": "Winning, Riegerweg/Altersheim",
            "sev": false,
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
            "live": false,
            "delay": 0,
            "cancelled": false,
            "lineBackgroundColor": "#ea4029",
            "departureId": "07e4533ca5585437c959fdeb9980e3d1#1672060500000#de:09162:6",
            "sev": false,
            "platform": "",
            "stopPositionNumber": 0,
            "infoMessages": []
        },
		...
        {
            "departureTime": 1672060920000,
            "product": "UBAHN",
            "label": "U2",
            "destination": "Messestadt Ost",
            "live": false,
            "delay": 0,
            "cancelled": false,
            "lineBackgroundColor": "#dd3d4d",
            "departureId": "5c89169b4eac9e688234efa99532f10c#1672060920000#de:09162:6",
            "sev": false,
            "platform": "U2/8 Gleis 2",
            "stopPositionNumber": 0,
            "infoMessages": []
        },
		...
        {
            "departureTime": 1672060980000,
            "product": "SBAHN",
            "label": "S3",
            "destination": "Deisenhofen",
            "live": false,
            "delay": 1,
            "cancelled": false,
            "lineBackgroundColor": "#942d8d",
            "departureId": "0a78778e46079d11830c36fca7566b36#1672060980000#de:09162:6",
            "sev": false,
            "platform": "1",
            "stopPositionNumber": 0,
            "infoMessages": [
                "Linie S3: Maskenpflicht nach gesetzl. Regelung; wir empfehlen eine FFP2-Maske Linie S3: Fahrradmitnahme begrenzt möglich Linie S3: Bei Fahrradmitnahme Sperrzeiten beachten Linie S3: nur 2. Kl."
            ]
        },
		...
        {
            "departureTime": 1672060680000,
            "product": "BUS",
            "label": "59",
            "destination": "Ackermannbogen via Münchner Freiheit U",
            "live": false,
            "delay": 0,
            "cancelled": false,
            "lineBackgroundColor": "#0d5c70",
            "departureId": "0b10f46a89dc6a150f5db24e7ca26f14#1672060680000#de:09162:1110",
            "sev": false,
            "platform": "Pos. 7",
            "stopPositionNumber": 7,
            "infoMessages": []
        },
		...
        {
            "departureTime": 1672061100000,
            "product": "REGIONAL_BUS",
            "label": "220",
            "destination": "Winning, Riegerweg/Altersheim",
            "live": false,
            "delay": 0,
            "cancelled": false,
            "lineBackgroundColor": "#0d5c70",
            "departureId": "14d5f38f4e1169b03e25752dd25259f5#1672061100000#de:09162:1110",
            "sev": false,
            "platform": "Pos. 10",
            "stopPositionNumber": 10,
            "infoMessages": []
        }
    ]
}
```



See https://www.mvv-muenchen.de/fahrplanauskunft/fuer-entwickler/opendata/index.html for more information.