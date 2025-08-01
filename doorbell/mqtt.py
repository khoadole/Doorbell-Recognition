import paho.mqtt.client as mqtt
from django.conf import settings
from .models import DeviceLog
from users.utils import sendDoorBell
from .FacialEmbeddingsModel import recognize_face, preprocess_image, enbedding_image
import json
import socket

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
        # print(f"[MQTT] Message received on {msg.topic}: {data}")

        if msg.topic == TOPIC_TO_SERVER:
            # Handle message from device
            handle_device_message(data)

    except json.JSONDecodeError:
        print("[MQTT] Invalid JSON received.")

def handle_device_message(data):
    if 'doorbell' in data:
        sendDoorBell()
        print("[MQTT] Handling device message: Somebody just hit the button")
    elif 'image' in data:
        if data['image'] is None:
            publish_to_device("opendoor", False)
            print(f"[MQTT] Handling device message: No image")
            return   
        print(f"[MQTT] Handling device message: Face detection")

        preprocessed_image = preprocess_image(data['image'], detect=True)
        if preprocessed_image is None:
            publish_to_device("opendoor", False)
            return 
        embedding = enbedding_image(preprocessed_image)
        name, score = recognize_face(embedding)
        recognize = True if score >= 0.8 else False
        print(f"FACE RECOGNITION threshold: {score} - {name}")         

        log = DeviceLog(
            name = name,
            percent = score,
            status = recognize,
            image = data["image"]
        )
        log.save()
        publish_to_device("opendoor", recognize)   
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