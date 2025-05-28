from . import views
from django.urls import path


app_name = "accounts"
urlpatterns = [
    path("register/",views.UserRegisterView.as_view(),name="register"),
    path("verify_code/",views.UserVerifyRegisterCodeView.as_view(),name="verify_code"),
    path("resend_code/",views.ResendOtpCodeView.as_view(),name="resend_code"),
    path("login/",views.UserLoginView.as_view(),name="login"),
    path("logout/",views.UserLogoutView.as_view(),name="logout"),
    path("reset/",views.UserPasswordResetView.as_view(),name='passowrd_reset') , 
    path("reset/done/",views.UserPaswwordResetDoneView.as_view(),name='password_reset_done') ,
    path("reset/confirm/<uidb64>/<token>/",views.UserPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path("reset/complete/",views.UserPasswordResetCompleteView.as_view(),name="password_reset_complete")
]