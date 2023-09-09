from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import UserConfig


def send_email(instance, unique_token, link, subject, message):
    try:
        # Get the user related config and save the token.
        conf = UserConfig.objects.filter(user=instance).first()
        conf.token = unique_token
        conf.generation_time = datetime.now()
        conf.save()

        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])
        return "Mail sent successfully."
    except Exception as e:
        return str("Error:", str(e))
