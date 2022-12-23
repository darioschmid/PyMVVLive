from mvv_sbahn import punctuality
import re


def test_get_departures():
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        assert any(re.findall("(\d+ %)", punctuality.punctuality(line)))
    assert any(re.findall("(\d+ %)", punctuality.punctuality("S20"))) or punctuality.punctuality("S20") == "-"
