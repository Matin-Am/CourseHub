from celery import shared_task
from django.core.mail import send_mail



@shared_task
def send_otp_code(code,email):
    subject = "Your otp code"
    message = f"Your otp code is: {code}"
    sender_email = "matin.amani101013@gmail.com"
    recipient_list = [email]

    send_mail(subject,message,sender_email,recipient_list)
