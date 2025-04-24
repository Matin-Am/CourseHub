from . import api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView , TokenObtainPairView

urlpatterns = [
    path("register/",api_views.UserRegistrationAPI.as_view()),
    path("verify_code/",api_views.UserVerifyCodeAPI.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
