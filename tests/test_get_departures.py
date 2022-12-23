from mvv_sbahn import get_departures
import json


def test_get_departures():
    departures = get_departures.get_departures("Unterhaching", destination_blacklist=["Holzkirchen"])
    print(json.dumps(departures, indent=4, sort_keys=True))
    assert isinstance(get_departures.get_departures("Unterhaching"), list)
