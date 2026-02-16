from django.core.management.base import BaseCommand,CommandError
from datetime import datetime , timedelta
import pytz
from accounts.models import OtpCode

class Command(BaseCommand):
    help = "removing all expird otp codes"
    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) + timedelta(minutes=3)
        expired_codes = OtpCode.objects.filter(created__lt=expired_time)
        if expired_codes.exists():
            expired_codes.delete()
            self.stderr.write(self.style.WARNING("Otp Codes have been removed."))
        else:
            raise CommandError("No otp codes exists !")