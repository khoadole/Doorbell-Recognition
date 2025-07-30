from mongoengine import Document, StringField, DateField, ReferenceField, FloatField, BooleanField, DateTimeField
from users.models import User
import datetime

# Create your models here.

class Device(Document):
    serial = StringField(required=True)
    name = StringField()
    owner = ReferenceField(User, required=True)
    date_add = DateField(default=datetime.datetime.now)

class DeviceLog(Document):
    # device = ReferenceField(Device, required=True)
    name = StringField(default="Unknown Person")
    percent = FloatField(required=True)
    status = BooleanField(default=False)
    date_add = DateTimeField(default=datetime.datetime.now)
    image = StringField()
    
class EnrolledFace(Document):
    name = StringField(required=True)
    image = StringField(required=True)  # base64 encoded image
    create_at = DateTimeField(default=datetime.datetime.now)
    type = StringField(default="enrolled_face")
    # owner = ReferenceField(User, required=True)  # Link to user who uploaded
    
    meta = {
        'collection': 'enrolled_faces',
        'ordering': ['-create_at']
    }