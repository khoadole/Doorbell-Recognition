import cv2
import requests
import time

SERVER_URL = "http://127.0.0.1:8000/api/upload_frame"

cap = cv2.VideoCapture(0)  # 0 for default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, jpeg = cv2.imencode('.jpg', frame)
    try:
        response = requests.post(SERVER_URL, data=jpeg.tobytes(), headers={
            "Content-Type": "image/jpeg"
        })
        print("Sent frame:", response.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(0.1)

cap.release()