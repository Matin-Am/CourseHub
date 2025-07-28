from django.test import TestCase
from accounts.forms import UserRegistrationForm , UserLoginForm , UserReigisterVerifyCodeForm
from django.contrib.auth import get_user_model
from accounts.models import OtpCode


class TestUserRegistrationForm(TestCase):
    def test_valid_data(self):
        form = UserRegistrationForm(data={"username":"matin","email":"matin@email.com","password":"matin","password2":"matin"})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_data(self):
        form = UserRegistrationForm(data={"username":"matin","email":"invalid","password":"matin","password2":"matin"})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("email"))
        self.assertIn("Enter a valid email address.",form.errors["email"])

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertEqual(len(form.errors),4)
        self.assertFalse(form.is_valid())


    def test_exists_username(self):
        OtpCode.objects.create(code=1234 , email="matin@email.com")
        get_user_model().objects.create_user(username='matin',email="matin@email.com",password="matin")
        form = UserRegistrationForm(data={"username":"matin","email":"matinn@email.com","password":"matin","password2":"matin"})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertTrue(form.has_error("username"))
        self.assertIn("This user with this username already regsitered ! " , form.errors["username"])

    def test_exists_email(self):
        OtpCode.objects.create(code=1234 , email="matin@email.com")
        get_user_model().objects.create_user(username='matin',email="matin@email.com",password="matin")
        form = UserRegistrationForm(data={"username":"Matin-Am","email":"matin@email.com","password":"matin","password2":"matin"})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("email"))
        self.assertIn("This user with this email already regsitered ! " , form.errors["email"])



    def test_matched_passwords(self):
        form = UserRegistrationForm(data={"username":"Matin-Am","email":"matin@email.com","password":"matin","password2":"majid"})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertIn("Passwords must match ! " , form.errors["__all__"])
        self.assertTrue(form.has_error("__all__"))



class TestUserReigisterVerifyCodeForm(TestCase):
    def test_valid_data(self):
        form = UserReigisterVerifyCodeForm(data={"code":1234})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_error("code"))
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = UserReigisterVerifyCodeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("code"))
        
