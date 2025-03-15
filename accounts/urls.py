from . import views
from django.urls import path


app_name = "accounts"
urlpatterns = [
    path("register/",views.UserRegisterView.as_view(),name="register"),
]