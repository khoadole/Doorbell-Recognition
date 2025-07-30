from django.conf import settings
from .models import EnrolledFace
from tensorflow.keras.models import load_model, Model
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

def preprocess_image(base64_str):
    # Decode base64 to bytes
    img_data = base64.b64decode(base64_str)

    # Convert bytes to numpy array (uint8)
    nparr = np.frombuffer(img_data, np.uint8)

    # Decode image from numpy array (OpenCV format)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize and normalize
    img = cv2.resize(img, (224, 224)) # Change 96x96 later
    img = img.astype('float32') / 255.0

    return np.expand_dims(img, axis=0)  # shape: (1, 224, 224, 3)

def enbedding_image(image):
    return embedding_model.predict(image)

def cosine_similarity(a, b):
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_face(image_base64):
    best_match = "Unknown"
    best_score = -1
    embedding = enbedding_image(preprocess_image(image_base64))

    for face in EnrolledFace.objects():
        name = face.name
        embedding_stored = enbedding_image(preprocess_image(face.image))
        
        sim = cosine_similarity(embedding, embedding_stored)
        if sim > best_score:
            best_match = name
            best_score = sim

    return best_match, best_score

