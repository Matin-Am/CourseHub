from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_otp_code(code, email):
    try:
        subject = "Your otp code"
        message = f"Your otp code is: {code}"
        sender_email = "matin.amani101013@gmail.com"
        recipient_list = [email]
        send_mail(subject, message, sender_email, recipient_list)

        print(f"[✓] Email sent to {email} with code {code}")  # برای نمایش در ترمینال
        logger.info(f"OTP code {code} sent to {email}")        # برای لاگ در فایل یا جاهای دیگه
    except Exception as e:
        print(f"[✗] Failed to send email: {e}")
        logger.error(f"Failed to send OTP code to {email}: {e}")
