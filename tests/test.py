import MVVLive
import json

stop_name = "Unterhaching"
stop_id = "de:09184:2310"
line = "S3"

def test(live):
    try:
        print(live.punctuality)
    except:
        print("No punctuality data available")

    try:
        data = json.dumps(live.data, indent=4, ensure_ascii=False)
        #print(data)
    except:
        print("No data available")

    try:
        departures = json.dumps(live.departures, indent=4, ensure_ascii=False)
        #print(departures)
    except:
        print("No departures available")

    try:
        serving_lines = json.dumps(live.serving_lines, indent=4, ensure_ascii=False)
        #print(serving_lines)
    except:
        print("No serving lines available")

if __name__ == "__main__":
    live = MVVLive.MVVLive(stop_name=stop_name)
    test(live)
    live = MVVLive.MVVLive(stop_id=stop_id)
    test(live)
    live = MVVLive.MVVLive(line=line)
    test(live)
