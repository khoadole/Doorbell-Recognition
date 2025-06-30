from mongoengine import Document, StringField, FileField, EmailField, DateField
import datetime


# Create your models here.

def upload_path_handle(instance, filename):
    return 'users/{id}/{file}'.format(id=instance, file=filename)

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    phonenumber = StringField()
    address = StringField()
    email = EmailField()
    avatar = FileField()
    create_at = DateField(default=datetime.datetime.now)
