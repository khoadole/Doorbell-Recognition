from . import mqtt
from . import FacialEmbeddingsModel

mqtt.start()
FacialEmbeddingsModel.init()