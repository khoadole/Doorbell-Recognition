import paho.mqtt.client as mqtt
from django.conf import settings
import json
import threading
import time

TOPIC_TO_SERVER = f"{settings.MQTT_TOPIC}/to_server"
TOPIC_TO_DEVICE = f"{settings.MQTT_TOPIC}/to_device"

# MQTT client instance
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(TOPIC_TO_SERVER)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"[MQTT] Message received on {msg.topic}: {data}")

        if msg.topic == TOPIC_TO_SERVER:
            # Handle message from device
            handle_device_message(data)

    except json.JSONDecodeError:
        print("[MQTT] Invalid JSON received.")

def handle_device_message(data):
    # You can log to DB or trigger signals here
    print(f"[MQTT] Handling device message: {data}")

def start():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
    print("[MQTT] MQTT client Started!")
    client.loop_start()

def publish_to_device(command):
    payload = {
        "command": command
    }
    # print(client.is_connected())
    client.publish(TOPIC_TO_DEVICE, json.dumps(payload))
    print(f"[MQTT] Published to {TOPIC_TO_DEVICE}: {payload}")