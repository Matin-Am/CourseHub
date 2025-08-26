from django.test import SimpleTestCase
from django.urls import reverse,resolve
from ..views import(UserRegisterView,UserLoginView,UserVerifyRegisterCodeView,ResendOtpCodeView,UserLogoutView,
                    UserPasswordResetView,UserPaswwordResetDoneView,UserPasswordResetCompleteView,
                    UserPasswordResetConfirmView)


class TestAccountUrls(SimpleTestCase):
    def test_register_url(self):
        url = reverse("accounts:register")
        self.assertEqual(resolve(url).func.view_class,UserRegisterView)
    
    def test_verify_code_url(self):
        url = reverse("accounts:verify_code")
        self.assertEqual(resolve(url).func.view_class,UserVerifyRegisterCodeView)
    
    def test_resend_code_url(self):
        url = reverse("accounts:resend_code")
        self.assertEqual(resolve(url).func.view_class,ResendOtpCodeView)

    def test_login_url(self):
        url = reverse("accounts:login")
        self.assertEqual(resolve(url).func.view_class,UserLoginView)

    def test_logout_url(self):
        url = reverse("accounts:logout")
        self.assertEqual(resolve(url).func.view_class,UserLogoutView)

    def test_reset_url(self):
        url = reverse("accounts:password_reset")
        self.assertEqual(resolve(url).func.view_class,UserPasswordResetView)
    
    def test_reset_done_url(self):
        url = reverse("accounts:password_reset_done")
        self.assertEqual(resolve(url).func.view_class,UserPaswwordResetDoneView)

    def test_reset_confirm_url(self):
        url = reverse("accounts:password_reset_confirm",kwargs={"uidb64":"test_uidb64","token":"test_token"})
        self.assertEqual(resolve(url).func.view_class,UserPasswordResetConfirmView)

    def test_reset_complete_url(self):
        url = reverse("accounts:password_reset_complete")
        self.assertEqual(resolve(url).func.view_class,UserPasswordResetCompleteView)
        

