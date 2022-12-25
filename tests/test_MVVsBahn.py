import MVVsBahn
import re


def test_MVVsBahn():
    obj = MVVsBahn.MVVsBahn()
    for line in ["S1", "S2", "S3", "S4", "S6", "S7", "S8"]:
        assert int(obj.get_punctuality(line)) in range(0, 101)
    assert obj.get_punctuality("S20") == "-" or int(obj.get_punctuality("S20")) in range(0, 101)
