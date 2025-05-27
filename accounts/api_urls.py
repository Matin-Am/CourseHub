from . import api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView , TokenObtainPairView , TokenBlacklistView

urlpatterns = [
    path("register/",api_views.UserRegistrationAPI.as_view()),
    path("verify_code/",api_views.UserVerifyCodeAPI.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]