from django.core.management.base import BaseCommand
from datetime import datetime , timedelta
import pytz
from accounts.models import OtpCode

class Command(BaseCommand):
    help = "removing all expird otp codes"
    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) + timedelta(minutes=3)
        expired_codes = OtpCode.objects.filter(created__lt=expired_time)
        expired_codes.delete()
