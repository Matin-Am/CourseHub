from django.test import TestCase
from ..models import User,OtpCode
from django.utils import timezone
from datetime import datetime , time , timedelta

class TestUserModel(TestCase):

    def test_str_method(self):
        user = User.objects.create_user(username="matin",email="matin@email.com",password="matin")
        self.assertEqual(str(user),"matin - matin@email.com")

class TestOtpCodeModel(TestCase):

    def test_str_method(self):
        otp_code = OtpCode.objects.create(code=123,email="matin@email.com")
        self.assertEqual(str(otp_code),"matin@email.com - 123")
    
    def test_is_expired_method(self):
        otp_code = OtpCode.objects.create(code=123,email="matin@email.com")
        otp_code.created = timezone.now() - timedelta(minutes=5)
        self.assertTrue(otp_code.is_expired())