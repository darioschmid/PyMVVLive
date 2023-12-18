import MVVLive
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
stop_id = "de:09184:2310"
line = "S3"


def test_stops():
    stops = MVVLive.get_stops(api_key=API_KEY)
    stops_data = json.dumps(stops, indent=4, ensure_ascii=False)
    print("stops received.")


def test_departures():
    live_instance = MVVLive.MVVLive(api_key=API_KEY, stop_id=stop_id)
    live_instance.update_departures()
    departures = json.dumps(live_instance.departures, indent=4, ensure_ascii=False)
    print("departures received.")

    return


def test_punctuality():
    live_instance = MVVLive.MVVLive(api_key=API_KEY, line=line)
    live_instance.update_punctuality()
    punctuality = live_instance.punctuality
    print("punctuality received.")


def test_messages():
    live_instance = MVVLive.MVVLive(api_key=API_KEY)
    live_instance.update_messages()
    messages = live_instance.messages
    print("punctuality received.")
