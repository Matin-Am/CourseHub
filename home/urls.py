from . import views
from django.urls import path


app_name = "home"
urlpatterns = [
    path("home/",views.HomeView.as_view(),name="home"),
    path("episodes/<slug:course_slug>/",views.HomeView.as_view(),name="episodes"),
    path("detail/<slug:vid_slug>/",views.VideoDetailView.as_view(),name="video") , 
]