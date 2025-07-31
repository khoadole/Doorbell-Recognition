from django.apps import AppConfig
import os


class DoorbellConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doorbell'

    def ready(self):
        # Only run in main process, not in Django autoreloader
        if os.environ.get('RUN_MAIN') == 'true':
            from . import mqtt
            from . import FacialEmbeddingsModel

            mqtt.start()
            FacialEmbeddingsModel.init()
