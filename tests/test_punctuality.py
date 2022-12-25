from mvv_sbahn import punctuality
import re


def test_punctuality():
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        assert int(punctuality.punctuality(line)) in range(0, 101)
    assert punctuality.punctuality("S20") == "-" or int(punctuality.punctuality("S20")) in range(0, 101)
