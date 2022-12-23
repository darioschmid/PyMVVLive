from mvv_sbahn import get_departures

def test_get_departures():
    assert isinstance(get_departures.get_departures("Unterhaching"), list)
