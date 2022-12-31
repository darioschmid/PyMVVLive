import MVVLive
import re


def test_MVVLive():
    station = "Garching Forschungszentrum"
    line="S3"
    live = MVVLive.MVVLive(stop_name=station, line=line)

    # Test get_punctuality
    assert live.punctuality in range(0, 101)

    # Test get_serving_lines
    whitelist_serving_lines = {
        "lineNumber": ["U6", "230", "X201"],
    }
    serving_lines = live.filter(live.serving_lines, whitelist=whitelist_serving_lines)
    assert isinstance(serving_lines, list)
    assert isinstance(serving_lines[0], dict)
    

    # Test get_departures
    station = "Höllriegelskreuth"
    blacklist_departures = {
        "product": ["REGIONAL_BUS"],
    }
    departures = live.filter(live.departures, blacklist=blacklist_departures)
    assert isinstance(departures, list)
    assert isinstance(departures[0], dict)
