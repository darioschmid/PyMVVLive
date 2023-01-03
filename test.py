import MVVLive
import json

stop_name = "Unterhaching"
stop_id = "de:09184:2310"
line = "S3"

def test(live):
    try:
        live.update_punctuality()
        print(live.punctuality)
    except:
        print("No punctuality data available")

    try:
        live.update_data()
        data = json.dumps(live.data, indent=4, ensure_ascii=False)
        print("data received.")
        #print(data)
    except:
        print("No data available")

    try:
        live.update_serving_lines()
        serving_lines = json.dumps(live.serving_lines, indent=4, ensure_ascii=False)
        print("serving_lines received.")
        #print(serving_lines)
    except:
        print("No serving lines available")

    try:
        live.update_departures()
        departures = json.dumps(live.departures, indent=4, ensure_ascii=False)
        print("departures received.")
        #print(departures)
    except:
        print("No departures available")

if __name__ == "__main__":
    live = MVVLive.MVVLive(stop_name=stop_name)
    print("Testing stop_name...")
    test(live)

    live = MVVLive.MVVLive(stop_id=stop_id)
    print("\nTesting stop_id...")
    test(live)

    live = MVVLive.MVVLive(line=line)
    print("\nTesting line...")
    test(live)
