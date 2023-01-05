import MVVLive
import json
from time import time



# Punctiality Demo
"""
Punctuality Demo
Get punctuality of line "S3".
"""

# Initialize MVVLive object with line
line = "S3"
live = MVVLive.MVVLive(line=line)

# Print punctuality
print(f"{line}: {live.punctuality} %")



"""
Serving Lines Demo
Get all serving lines at "Garching Forschungszentrum" station that are regional busses.
"""

# Initialize MVVLive object with stop ID
stop_id = "de:09184:460"  # stop ID of "Garching Forschungszentrum"
live = MVVLive.MVVLive(stop_id=stop_id)

# Filter serving lines
whitelist_serving_lines = {
    "product": ["REGIONAL_BUS"],
}
serving_lines = live.filter(live.serving_lines, whitelist=whitelist_serving_lines)

# Print serving lines in a nicely formatted way.
print(f"{stop_id} serving lines: {json.dumps(serving_lines, indent=4, ensure_ascii=False)}")



"""
Departures Demo
Get all departures from "Unterhaching" station that are in the next 30 minutes and not from the lines 217, 220 or 221.
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

# Print serving lines in a nicely formatted way.
print(f"{stop_name} departures: {json.dumps(departures, indent=4, ensure_ascii=False)}")

