from datetime import timedelta,datetime
from unittest import mock
from django.test import TestCase , Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from ..models import User,OtpCode
from ..forms import UserRegistrationForm,UserReigisterVerifyCodeForm,UserLoginForm


class TestUserRegisterView(TestCase):

    
    def test_redirect_home_if_authenticated(self):
        """
        redirects user to the home page if the user is authenticated
        """
        user = User.objects.create_user(username="matin",email="matin@email.com",password="matin")
        self.client.login(username="matin",password="matin")
        response = self.client.get(reverse("accounts:register"))
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)
    
    def test_GET_http_method(self):
        """
        test if rendering 'register.html' with its  matching form works correctly or not
        """
        response = self.client.get(reverse("accounts:register"))
        self.assertTemplateUsed(response,"accounts/register.html")
        self.assertIsInstance(response.context["form"],UserRegistrationForm)
        self.assertEqual(response.status_code,200)

    @mock.patch("accounts.views.send_otp")
    def test_valid_data_POST_http_method(self,mock_send_email):
        """
        test if user sends valid data or not 
        """
        SESSION_ID = "user_data"
        sent_data = {"username":"matin","email":"matin@email.com","password":"matin","password2":"matin"}
        response = self.client.post(reverse("accounts:register"),data=sent_data)
        self.assertEqual(OtpCode.objects.first().email,"matin@email.com")
        self.assertEqual(list(response.wsgi_request.session[SESSION_ID].keys())[0],"matin")
        self.assertEqual(response.wsgi_request.session[SESSION_ID].get(sent_data["username"]).get("email"),"matin@email.com")
        self.assertRedirects(response,reverse("accounts:verify_code"))
        self.assertEqual(response.status_code,302)
    
    @mock.patch("accounts.views.send_otp")
    def test_invalid_data_POST_http_method(self,mock_send_otp):
        """
        test when user sends invalid data
        """
        sent_data = {"username":"matin","email":"invalid_email","password":"matin","password2":"matin"}
        response = self.client.post(reverse("accounts:register"),data=sent_data)
        self.assertFalse(response.context["form"].is_valid())
        self.assertFormError(form=response.context["form"],field="email",errors=["Enter a valid email address."])
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"accounts/register.html")


class TestUserVerifyRegisterCodeView(TestCase):

    def setUp(self):
        self.username = "matin"
        self.email = "matin@email.com"
        self.password = "matin"
        session = self.client.session
        session["user_data"] = {
            self.username:{
                "email":self.email , 
                "password":self.password,
                "last_login":"2025-01-01 01:01:01"
            }
        }
        self.otp_code = OtpCode.objects.create(code=123,email="matin@email.com")
        
        session.save()
    def test_GET_http_method(self):
        """
        test if rendering 'verify_code.html' with its  matching form works correctly or not
        """
        response = self.client.get(reverse("accounts:verify_code"))
        self.assertTemplateUsed(response,"accounts/verify_code.html")
        self.assertIsInstance(response.context["form"],UserReigisterVerifyCodeForm)
        self.assertEqual(response.status_code,200)

    def test_otp_code_is_expired(self):
        """
        test if otp code is expired , user will be redirected to 'verify_code.html' for receiving another code
        """
        self.otp_code.created = timezone.now() - timedelta(minutes=5)
        self.otp_code.save()
        response = self.client.post(reverse("accounts:verify_code"),data={"code":123})
        self.assertTrue(self.otp_code.is_expired())
        self.assertRedirects(response,reverse("accounts:verify_code"))
        self.assertEqual(response.status_code,302)



    def test_valid_data_with_matching_code(self):
        """
        test if user sends valid data and verifies correct otp code 
        """
        response = self.client.post(reverse("accounts:verify_code"),data={"code":123})
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(OtpCode.objects.count(),0)
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"User has been created successfully")

    def test_valid_data_with_unmatching_code(self):
        """
        test if user sends valid data but verifies wrong code
        """
        response = self.client.post(reverse("accounts:verify_code"),data={"code":321})
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"code is wrong please try again !")
        self.assertRedirects(response,reverse("accounts:verify_code"))
        self.assertEqual(response.status_code,302)

    def test_invalid_data_POST(self):
        """
        test when user sends invalid data 
        """
        response = self.client.post(reverse("accounts:verify_code"),data={"code":"invalid_data"})
        self.assertIsInstance(response.context["form"],UserReigisterVerifyCodeForm)
        self.assertTemplateUsed(response,"accounts/verify_code.html")
        self.assertEqual(response.status_code,200)

class TestUserRegisterAndVerifyCodeFlow(TestCase):

    def setUp(self):
        self.client = Client()


    @mock.patch("accounts.views.send_otp")
    def test_register_and_verify(self,mock_send_otp):
        """
        test when user register and receives code , after verifying correct code an user will be created 
        in database.
        """
        sent_data = {"username":"matin","email":"matin@email.com","password":"matin","password2":"matin"}
        response = self.client.post(reverse("accounts:register"),data=sent_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("accounts:verify_code"))
        otp_code = OtpCode.objects.first()
        self.assertIsNotNone(otp_code)
        self.client.post(reverse("accounts:verify_code"),data={"code":otp_code.code})
        self.assertEqual(User.objects.count(),1)
        self.assertIsNone(OtpCode.objects.first())
        self.assertEqual(response.status_code,302)

class TestUserLoginView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="matin",email="matin@email.com",password="matin")
        self.url = reverse("accounts:login")

    def test_redirect_home_if_authenticated(self):
        """
        redirects user to the home page if the user is authenticated
        """
        self.client.login(username="matin",password="matin")
        response = self.client.get(self.url)
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)

    def test_GET_http_method(self):
        """
        test if rendering 'login.html' with its matching form works correctly or not
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response,"accounts/login.html")
        self.assertIsInstance(response.context["form"],UserLoginForm)
        self.assertEqual(response.status_code,200)

    def test_valid_data_with_wrong_info(self):
        """
        test when user sends valid data but his/her information is wrong 
        """
        data={"username":"wrong_username","password":"wrong_pass"}
        response = self.client.post(self.url,data=data)
        self.assertNotEqual(str(response.wsgi_request.user),"matin")
        self.assertEqual(str(response.wsgi_request.user),'AnonymousUser')
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"Username or password is wrong")
        self.assertRedirects(response,self.url)
        self.assertEqual(response.status_code,302)
    
    def test_valid_data_with_correct_info(self):
        """
        test when user sends valid data with correct information. 
        """
        data={"username":"matin","password":"matin"}
        response = self.client.post(self.url,data=data)
        self.assertEqual(str(response.wsgi_request.user.username),"matin")
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"User has been logged in successfully")
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)

    def test_invalid_data(self):
        """
        test when user sends invalid data
        """
        data={"username":"","password":"invalid_pass"}
        response = self.client.post(self.url,data=data)
        self.assertTemplateUsed(response,"accounts/login.html")
        self.assertIsInstance(response.context["form"],UserLoginForm)
        self.assertFormError(response.context["form"],"username","This field is required.")
        self.assertEqual(response.status_code,200)

class TestUserLogoutView(TestCase):
        
        def setUp(self):
            self.url = reverse("accounts:logout")
            self.user = User.objects.create_user(username="matin",email="matin@email.com",password="matin")
            self.client = Client()

        def test_redirect_login_page(self):
            """
            test if user is not authenticated it will redirect him/her to the login page 
            """
            response = self.client.get(self.url)
            self.assertRedirects(response,reverse("accounts:login")+"?next="+self.url)
            self.assertEqual(response.status_code,302)

        def test_log_user_out(self):
            """
            if user is authenticated he/she will be logged out. 
            """
            self.client.login(username="matin",password="matin")
            response = self.client.get(self.url)
            self.assertEqual(str(response.wsgi_request.user),"AnonymousUser")
            self.assertRedirects(response,reverse("home:home"))
            self.assertEqual(response.status_code,302)

class TestUserLoginAndLogoutViewFlow(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="matin",email="matin@email.com",password="matin")
        self.client = Client()

    def test_login_and_logout(self):
        """
        test user login and logout flow 
        """
        # log in user
        response = self.client.post(reverse("accounts:login"),data={"username":"matin","password":"matin"})
        self.assertEqual(str(response.wsgi_request.user.username),"matin")
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"User has been logged in successfully")
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)

        # log out user 
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(str(response.wsgi_request.user),"AnonymousUser")
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"User logged out successfully")
        self.assertRedirects(response,reverse("home:home"))
        self.assertEqual(response.status_code,302)

class TestResendOtpCodeView(TestCase):
    
    def setUp(self):
        session = self.client.session
        self.username = "matin"
        self.password = "matin"
        self.email = "matin@email.com"
        self.url = reverse("accounts:resend_code")
        self.otp_code = OtpCode.objects.create(email=self.email,code=1234)
        session["user_data"] = {
                self.username:{
                    "email":self.email,
                    "password":self.password,
                    "last_login":str(timezone.make_aware(datetime(2025,1,1,11,1,1)))
                }
            }
        session.save()


    @mock.patch("accounts.views.send_otp")
    def test_expired_code(self,mock_send_otp):
        """
        test if old code is expired , new code will be created and sent to the user 
        """
        self.otp_code.created = timezone.make_aware(datetime(2025,1,1,12,1,1))
        self.otp_code.save()
        response = self.client.get(self.url)    
        self.assertEqual(OtpCode.objects.count(),1)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"New code has been resend to your email")

    def test_not_expired_code(self):
        """
        test if old code is not expired,resend otp code won't be sent and a danger message will be showed
        """
        response = self.client.get(self.url)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"You cant resend code now")
    
    def test_no_otp_code(self):
        """
        test when no otp code would be found for the respective email 
        """
        client = Client()
        session = client.session
        session["user_data"] = {
            "test":{
                "email":"test@email.com", 
                "password":"test", 
                "last_login":str(timezone.make_aware(datetime(2025,1,1,12,1,1)))
            }
        }
        session.save()
        response = client.get(self.url)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]),"No otp code found for this email")
        

