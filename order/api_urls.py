from . import api_views
from django.urls import path




urlpatterns = [
    path("cart/",api_views.CartDetailAPI.as_view()),
    path("cart/add/<slug:course_slug>/",api_views.CartAddAPI.as_view()),
    path("cart/remove/<slug:course_slug>/", api_views.CartDeleteAPI.as_view())
]