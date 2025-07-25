from mongoengine import Document, StringField, DateField, ReferenceField, FloatField, BooleanField, DateTimeField
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
    # device = ReferenceField(Device, required=True)
    name = StringField(default="Unknown Person")
    percent = FloatField(required=True)
    status = BooleanField(default=False)
    date_add = DateTimeField(default=datetime.datetime.now)
    image = StringField()
    
