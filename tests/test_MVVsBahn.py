import MVVLive
import re


def test_MVVLive():
    live = MVVLive.MVVLive()


    # Test get_punctuality
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        assert live.get_punctuality(line) in range(0, 101)
    assert live.get_punctuality("S20") == "-" or int(live.get_punctuality("S20")) in range(0, 101)
    

    # Test get_serving_lines
    station = "Garching Forschungszentrum"
    whitelist_serving_lines = {
        "lineNumber": ["U6", "230", "X201"],
    }
    serving_lines = live.get_serving_lines(station, whitelist=whitelist_serving_lines)
    assert isinstance(serving_lines, list)
    assert isinstance(serving_lines[0], dict)
    

    # Test get_departures
    station = "Höllriegelskreuth"
    blacklist_departures = {
        "product": ["REGIONAL_BUS"],
    }
    departures = live.get_departures(station, blacklist=blacklist_departures)
    assert isinstance(departures, list)
    assert isinstance(departures[0], dict)
