#!/usr/bin/python3

import json
import math
import requests
import datetime
import sys
import paho.mqtt.client as mqtt
import logging


logging.basicConfig(filename='mvv_log.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s %(message)s')


logging.info("""
#########################################
########## Starting MVV Script ##########
#########################################""")

def print_s_bahn_departures(departures):
    """Prints the S-Bahn departures in a nice format"""
    departures = departures.copy()
    for departure in departures:
        del departure["departureId"]
        del departure["infoMessages"]
        del departure["label"]
        del departure["lineBackgroundColor"]
        del departure["live"]
        del departure["platform"]
        del departure["product"]
        del departure["sev"]
        del departure["stopPositionNumber"]
    for departure in departures:
        departure["departureTime"] = datetime.datetime.fromtimestamp(departure["departureTime"]/1000).strftime('%Y-%m-%d %H:%M:%S')
    logging.info("S-Bahn departures:")
    logging.info(json.dumps(departures, indent=4, sort_keys=True))


# setup mqtt
mqtt_broker="homeassistant"
mqtt_port=1883


response = requests.get("https://www.mvg.de/api/fahrinfo/departure/de:09184:2310?footway=0")
s_bahn_destination_wrong_direction = ["Taufkirchen", "Furth", "Deisenhofen", "Sauerlach", "Otterfing", "Holzkirchen"]
disruption_key_words = ["Verzögerung", "Verspätung", "Reparatur", "Stellwerk", "Weiche", "Störung"]


# exit if response is not 200
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit(1)


# print entire json response
departures = response.json()['departures']
#print("##############################################################################################################")
#print("json response:")
#print(json.dumps(departures, indent=4, sort_keys=True))


# delete all departures that are not S-Bahn or are in the blacklist
departures = [destination for destination in departures if destination["product"] == "SBAHN" and destination["destination"] not in s_bahn_destination_wrong_direction]


# determine if there are any disruptions
latestMessage = departures[0]["infoMessages"][0]
disruptions = sum([key_word in latestMessage for key_word in disruption_key_words])

# determine the maximum delay
delays = [departure["delay"] for departure in departures]
max_delay = max(delays)

# determine if there are any cancellations
cancelled = [departure["cancelled"] for departure in departures]
cancellations = str(sum(cancelled)) + "/" + str(len(cancelled))

# determine the reliability
unreliability = sum(cancelled)/len(departures) + max_delay/30 + disruptions/6
reliability = math.ceil(max((1 - unreliability) * 100, 0))


# print the departures
print_s_bahn_departures(departures)
logging.info(f"{latestMessage=}")
logging.info(f"{delays=}")
logging.info(f"{cancelled=}")
logging.info(f"==> {disruptions=}")
logging.info(f"==> {max_delay=}")
logging.info(f"==> {cancellations=}")
logging.info(f"==> {reliability=}")


# Send MQTT messages
client = mqtt.Client("ha-client")
client.username_pw_set(username="python_s_bahn_script",password="5qChAzNvVhihGqCmd23ej2Pxv")
client.connect(mqtt_broker, mqtt_port)
client.publish('home-assistant/SBahn/max_delay', max_delay)
client.publish('home-assistant/SBahn/disruptions', disruptions)
client.publish('home-assistant/SBahn/cancellations', cancellations)
client.publish('home-assistant/SBahn/reliability', reliability)
