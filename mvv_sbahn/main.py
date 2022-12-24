import punctuality
import mqtt_publish
import get_departures
import math
import logging
#import json
# DELETEME
import paho.mqtt.client as mqtt

# DELETEME
MQTT_BROKER = "homeassistant"
MQTT_PORT = 1883
client = mqtt.Client("ha-client")
client.username_pw_set(username="python_s_bahn_script",  password="5qChAzNvVhihGqCmd23ej2Pxv")
client.connect(MQTT_BROKER, MQTT_PORT)

logging.basicConfig(filename='mvv_sbahn.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s %(message)s')

destination_blacklist = ["Taufkirchen", "Furth", "Deisenhofen", "Sauerlach", "Otterfing", "Holzkirchen"]
disruption_key_words = ["Verzögerung", "Verspätung", "Reparatur", "Stellwerk", "Weiche", "Störung"]

departures = get_departures.get_departures("Unterhaching", destination_blacklist=destination_blacklist)

#print(json.dumps(departures, indent=4, sort_keys=True))

# determine if there are any disruptions
latestMessage = departures[0]["infoMessages"][0]
disruptions = sum([key_word in latestMessage for key_word in disruption_key_words])

# determine the maximum delay
delays = [departure.get("delay", 0) for departure in departures]
max_delay = max(delays)

# determine if there are any cancellations
cancelled = [departure.get("cancelled", False) for departure in departures]
cancellations = str(sum(cancelled)) + "/" + str(len(cancelled))

# determine the reliability
unreliability = sum(cancelled)/len(departures) + max_delay/30 + disruptions/6
reliability = math.ceil(max((1 - unreliability) * 100, 0))

# scprape punctuality
punctuality = punctuality.punctuality("S3")

# publish mqtt messages
#publications = {
#    "punctuality": punctuality,
#    "disruptions": disruptions,
#    "cancellations": cancellations,
#    "reliability": reliability,
#    "max_delay": max_delay,
#}
#mqtt_publish.publish(publications)
#mqtt_publish.publish("punctuality", str(punctuality))
#mqtt_publish.publish("disruptions", str(disruptions))
#mqtt_publish.publish("cancellations", str(cancellations))
#mqtt_publish.publish("reliability", str(reliability))
#mqtt_publish.publish("max_delay", str(max_delay))
#mqtt_publish.disconnect()

# Logging the results
logging.info(f"{punctuality=}")
logging.info(f"{disruptions=}")
logging.info(f"{max_delay=}")
logging.info(f"{cancellations=}")
logging.info(f"{reliability=}")

# DELETEME
message = client.publish("home-assistant/SBahn/disruptions", disruptions)
message.wait_for_publish()
message = client.publish("home-assistant/SBahn/punctuality", punctuality)
message.wait_for_publish()
message = client.publish("home-assistant/SBahn/max_delay", max_delay)
message.wait_for_publish()
message = client.publish("home-assistant/SBahn/cancellations", cancellations)
message.wait_for_publish()
message = client.publish("home-assistant/SBahn/test", cancellations)
message.wait_for_publish()
message = client.publish("home-assistant/SBahn/reliability", reliability)
message.wait_for_publish()

client.disconnect()