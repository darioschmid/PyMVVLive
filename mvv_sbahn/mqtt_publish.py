import paho.mqtt.client as mqtt

MQTT_BROKER = "homeassistant"
MQTT_PORT = 1883


client = mqtt.Client("ha-client")
client.username_pw_set(username="python_s_bahn_script",  password="5qChAzNvVhihGqCmd23ej2Pxv")
client.connect(MQTT_BROKER, MQTT_PORT)

def publish(key, value):
    #for key, value in publications.items():
    #    message = client.publish("home-assistant/SBahn/" + key, value)
    #    message.wait_for_publish()
    #    print(message.is_published())
    message = client.publish("home-assistant/SBahn/" + key, value)
    message.wait_for_publish()
    print(f"{message.is_published()=}")

def disconnect():
    disc = client.disconnect()
    print(disc)
    #disc.wait_for_disconnect()
    pass
