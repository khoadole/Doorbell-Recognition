import paho.mqtt.client as mqtt
from django.conf import settings
from .models import DeviceLog
from .FacialEmbeddingsModel import recognize_face
import json
import socket

TOPIC_TO_SERVER = f"{settings.MQTT_TOPIC}/to_server"
TOPIC_TO_DEVICE = f"{settings.MQTT_TOPIC}/to_device"

# MQTT client instance
client = mqtt.Client()
name = "Unknown"
score = 0

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(TOPIC_TO_SERVER)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        # print(f"[MQTT] Message received on {msg.topic}: {data}")

        if msg.topic == TOPIC_TO_SERVER:
            # Handle message from device
            handle_device_message(data)

    except json.JSONDecodeError:
        print("[MQTT] Invalid JSON received.")

def handle_device_message(data):
    global name
    global score
    if 'image' in data:
        ending = data["end"]
        print(f"[MQTT] Handling device message: Image - {ending}")
        

        if data["end"] == False:
            name, score = recognize_face(data['image'])

            # For saving image from device
            # import base64
            # import uuid
            # img = base64.b64decode(data['image'])
            # filename = f"saved_image/{uuid.uuid4()}.jpg"
            # with open(filename, 'wb') as f:
            #     f.write(img)

            if score >= 0.9:
                log = DeviceLog(
                    name = name,
                    percent = score,
                    status = True,
                    image = data["image"]
                )
                log.save()
                publish_to_device("opendoor", True)
                return        
        else:
            log = DeviceLog(
                name = name,
                percent = score,
                status = False,
                image = data["image"]
            )
            log.save()

    elif 'ip' in data:
        print(f"[MQTT] Handling device message: ip server request")
        ip = f"http://{get_computer_ipv4()}:8000/api/upload_frame"
        publish_to_device("ip", ip)
    else:
        print(f"[MQTT] Handling device message: {data}")


def start():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
    print("[MQTT] MQTT client Started!")
    client.loop_start()

def publish_to_device(name, command):
    payload = {
        name: command
    }
    # print(client.is_connected())
    client.publish(TOPIC_TO_DEVICE, json.dumps(payload))
    print(f"[MQTT] Published to {TOPIC_TO_DEVICE}: {payload}")

def get_computer_ipv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to any public IP address (Google DNS here)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip