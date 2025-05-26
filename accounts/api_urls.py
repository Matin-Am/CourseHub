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

'''

    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODcxOTc0MSwiaWF0IjoxNzQ4Mjg3NzQxLCJqdGkiOiJkMDg2YTkwZjRiYzY0MWJjOWE4NmNkOTA0ZjcwMDg1ZCIsInVzZXJfaWQiOjF9.sk9GdhDtXmcP36IHbkfowqBLslDDVUqJ1Q6NlbErPcI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4Mzc0MTQxLCJpYXQiOjE3NDgyODc3NDEsImp0aSI6ImQ4YWM3MDIwMjFlZjRiOTZiNzg4NDUyZjNkNjZmOTdjIiwidXNlcl9pZCI6MX0.WQyVNwKNArBkKK8XihpY7-KagdCvovDLwdc-n2vDmFg"
}
'''