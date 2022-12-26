import MVVLive
import json

# Initializing MVVLive object
live = MVVLive.MVVLive()


# Punctiality Demo
line = "S3"
print(f"{line}: {live.get_punctuality(line)} %")


# Serving Lines Demo
station = "Garching Forschungszentrum"
whitelist_serving_lines = {
    "lineNumber": ["U6", "230", "X201"],
}
serving_lines = live.get_serving_lines(stop_name=station, whitelist=whitelist_serving_lines)
print(f"{station} serving lines: {json.dumps(serving_lines, indent=4, sort_keys=True)}")


# Departues Demo
station = "Höllriegelskreuth"
blacklist_departures = {
    "product": ["REGIONAL_BUS"],
}
departures = live.get_departures(stop_name=station, blacklist=blacklist_departures)
print(f"{station} departures: {json.dumps(departures, indent=4, sort_keys=True)}")
