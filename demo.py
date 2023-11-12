import MVVLive
import json
from time import time

API_KEY = 'your_api_key'



"""
Punctuality Demo
Get punctuality of line "S3".
"""

# Initialize MVVLive object with line
line = "S3"
live = MVVLive.MVVLive(api_key=API_KEY, line=line)

# Print punctuality
print(f"{line}: {live.punctuality} %")



"""
Departures Demo
Get all departures from "Unterhaching" station that are in the next 30 minutes 
and not from the lines 217, 220 or 221.
"""

# Initialize MVVLive object with stop name
stop_id = "de:09184:2310"
live = MVVLive.MVVLive(api_key=API_KEY, stop_id=stop_id)

# Filter departures
in_30_min = round((time()+30*60)*1000)
blacklist_departures = {
    "destination": ["Deisenhofen", "Holzkirchen"],
}
whitelist_departures = {
    "label": ["S3"],
    "realtimeDepartureTime": range(in_30_min),
}
departures = live.filter(live.departures, whitelist=whitelist_departures,
                         blacklist=blacklist_departures)

# Print serving lines in a nicely formatted way.
print(f"{stop_id} departures: {json.dumps(departures, indent=4, ensure_ascii=False)}")
