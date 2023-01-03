import MVVLive
from time import time


def test_MVVLive():
    """
    Punctuality Test
    """
    # Combination: all but line is None
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        live = MVVLive.MVVLive(line=line)
        assert live.punctuality in range(0, 101)
        del live



    """
    Serving Lines Test
    """

    # Initialize MVVLive object with stop ID
    stop_id = "de:09184:460"  # stop ID of "Garching Forschungszentrum"
    live = MVVLive.MVVLive(stop_id=stop_id)

    # Filter serving lines
    whitelist_serving_lines = {
        "product": ["REGIONAL_BUS"],
    }
    serving_lines = live.filter(live.serving_lines, whitelist=whitelist_serving_lines)
    assert isinstance(serving_lines, list)
    assert isinstance(serving_lines[0], dict)



    """
    Departures Test
    """

    # Initialize MVVLive object with stop name
    stop_name = "Unterhaching"
    live = MVVLive.MVVLive(stop_name=stop_name)

    # Filter departures
    in_30_min = round((time()+30*60)*1000)
    blacklist_departures = {
        "destination": ["Deisenhofen", "Holzkirchen"],
    }
    whitelist_departures = {
        "label": ["S3"],
        "departureTime": range(in_30_min),
    }
    departures = live.filter(live.departures, whitelist=whitelist_departures, blacklist=blacklist_departures)
    assert isinstance(departures, list)
    assert isinstance(departures[0], dict)


if __name__ == "__main__":
    test_MVVLive()
