import MVVLive
import re


def test_MVVLive():
    obj = MVVLive.MVVLive()

    # Test get_punctuality
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        assert obj.get_punctuality(line) in range(0, 101)
    assert obj.get_punctuality("S20") == "-" or int(obj.get_punctuality("S20")) in range(0, 101)
    
    # Test get_data
    data = obj.get_data("Hauptbahnhof")
    assert isinstance(data, dict)
    assert isinstance(data["servingLines"], list)
    assert isinstance(data["servingLines"][0], dict)
    assert isinstance(data["departures"], list)
    assert isinstance(data["departures"][0], dict)
