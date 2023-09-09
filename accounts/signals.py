import uuid

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import UserProfile, UserConfig
from config.email import send_email


@receiver(post_save, sender=User)
def create_user_profile_and_config(instance, sender: User, created: bool, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserConfig.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def send_user_verification_email(instance, sender: User, created: bool, **kwargs):
#     if not instance.is_active:
#         # Generate a unique token for this user.
#         unique_token = uuid.uuid4()
#         # email logic
#         verification_link = f'http://localhost:8000/api/verify/?token={unique_token}'
#
#         subject = "Account Verification"
#         message = f"""
#                     Click on the link below to verify your account.
#
#                     {verification_link}
#                     """
#         send_email(instance, unique_token, verification_link, subject, message)
