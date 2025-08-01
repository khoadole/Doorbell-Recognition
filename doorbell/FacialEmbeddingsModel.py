from django.conf import settings
from .models import EnrolledFace
from tensorflow.keras.models import load_model, Model
from mtcnn import MTCNN
import cv2
import numpy as np
import base64

MODEL_PATH = str(settings.BASE_DIR) + '/vggface_finetuned.keras'
model = None
embedding_model = None

def init():
    global model
    global embedding_model
    model = load_model(MODEL_PATH)
    embedding_layer = model.get_layer(index=-2).output # Second to last layer
    embedding_model = Model(inputs=model.input, outputs=embedding_layer)
    print(model.summary())

def preprocess_image(base64_str, detect=False):
    # Decode base64 to bytes
    img_data = base64.b64decode(base64_str)

    # Convert bytes to numpy array (uint8)
    nparr = np.frombuffer(img_data, np.uint8)

    # Decode image from numpy array (OpenCV format)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR format
    if img is None:
        raise ValueError("Image decoding failed.")

    # Use MTCNN to detect face
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    faces = detector.detect_faces(img_rgb)

    if faces:
        # Get the first face box
        x, y, w, h = faces[0]['box']
        x, y = max(0, x), max(0, y)
        img = img[y:y+h, x:x+w]
    else:  
        print("[FACE CROPPING] No face detected in the image.")

    # Resize to 96x96 (VGGFace requirement)
    img = cv2.resize(img, (96, 96))

    # # For saving image from device
    # import uuid
    # filename = f"saved_image/{uuid.uuid4()}.jpg"
    # cv2.imwrite(filename, img)   

    # Convert to float32
    img = img.astype('float32')

    # Subtract VGGFace BGR mean
    mean = np.array([93.5940, 104.7624, 129.1863], dtype=np.float32)
    img -= mean

    # Add batch dimension
    return np.expand_dims(img, axis=0)  # shape: (1, 96, 96, 3)

def enbedding_image(image):
    return embedding_model.predict(image)

def cosine_similarity(a, b):
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_face(embedding):
    best_match = "Unknown"
    best_score = 0

    for face in EnrolledFace.objects():
        name = face["name"]
        embedding_stored = np.array(face["embedding"], dtype=np.float32)
        
        sim = cosine_similarity(embedding, embedding_stored)
        if sim > best_score:
            best_match = name
            best_score = sim

    return best_match, best_score

