from django.db.models.signals import post_save
from django.dispatch import receiver
from api import models  # Assuming you're using Django's built-in User model

from decouple import config
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=models.User)
def send_confirmation_email(sender, instance, created, **kwargs):
    print(instance, sender)
    if created:
        try:
            msg = EmailMultiAlternatives(
                'Confirm Your Email Code',
                f'OTP code use it to confirm your email: {instance.generate_otp()}',
                config('EMAIL_HOST_USER'),
                [instance.email]
            )
            # msg.attach_alternative(html_body, "text/html")
            msg.send()
            return True
        except ConnectionRefusedError as e:
            return False
