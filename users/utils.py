from django.conf import settings
from .models import OtpToken, User
from django.core.mail import send_mail
import secrets
from datetime import datetime, timedelta

# # Delete old Avatar image
# @receiver(models.signals.pre_save, sender=User)
# def auto_delete_material(sender, instance, **kwargs):
#     if not instance.pk:
#         return False
#     try:
#         old_avatar = sender.objects.get(pk=instance.pk).avatar
#     except sender.DoesNotExist:
#         return False
    
#     new_avatar = instance.avatar
#     if not old_avatar == new_avatar and old_avatar.name != 'users/avatar.svg':
#         if os.path.isfile(old_avatar.path):
#             os.remove(old_avatar.path)

def sendOtp(user):
    otp = OtpToken.objects(user=user.email).first()
    if not otp:
        otp = OtpToken(user=user.email)

    otp.otp_code = secrets.token_hex(3)
    otp.created_at = datetime.now()
    otp.expires_at = otp.created_at + timedelta(minutes=5)
    otp.save()

    subject = "Email Verification"
    message = f"""
                    Hi {user.username}, here is your OTP: {otp.otp_code}, it will expire in 5 minutes.
    """
    
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email,]
    send_mail(subject, message, sender, receiver, fail_silently=False)
    print("[EMAIL] OTP sended!")

def sendDoorBell():
    users = User.objects()

    subject = "Email Verification"
    message = f"""
                    Hi, someone just hit the button. Please check the camera on the website
    """
    
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email for user in users]
    send_mail(subject, message, sender, receiver, fail_silently=False)

    print("[EMAIL] notification sended!")