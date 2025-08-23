from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import OtpCode


# @receiver(signal=signals.post_save , sender=get_user_model())
# def remove_otp(sender , **kwargs):
#     if kwargs["created"]:
#         OtpCode.objects.get(email=kwargs["instance"].email).delete()