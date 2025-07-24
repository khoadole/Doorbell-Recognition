from mongoengine import Document, StringField, FileField, EmailField, DateField, DateTimeField
import datetime


# Create your models here.

def upload_path_handle(instance, filename):
    return 'users/{id}/{file}'.format(id=instance, file=filename)

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    phonenumber = StringField()
    address = StringField()
    email = EmailField(unique=True)
    avatar = FileField()
    create_at = DateField(default=datetime.datetime.now)

class OtpToken(Document):
    user = EmailField(unique=True)
    otp_code = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    expires_at = DateTimeField()