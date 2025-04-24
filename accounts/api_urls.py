from . import api_views
from django.urls import path


urlpatterns = [
    path("register/",api_views.UserRegistrationAPI.as_view()),
    path("verify_code/",api_views.UserVerifyCodeAPI.as_view()),
]