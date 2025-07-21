from mongoengine import Document, StringField, DateField, ReferenceField, FloatField, BinaryField
from users.models import User
import datetime

# Create your models here.

class Device(Document):
    serial = StringField(required=True)
    name = StringField()
    owner = ReferenceField(User, required=True)
    date_add = DateField(default=datetime.datetime.now)

class FaceID(Document):
    name = StringField(required=True)
    device = ReferenceField(Device, required=True)
    date_add = DateField(default=datetime.datetime.now)

class DeviceLog(Document):
    device = ReferenceField(Device, required=True)
    name = StringField(default="Unknown Person")
    percent = FloatField(required=True)
    date_add = DateField(default=datetime.datetime.now)
    image = BinaryField()
    
