from . import api_views
from django.urls import path




urlpatterns = [
    path("course/",api_views.CourseListAPI.as_view()),
    path("course/<slug:course_slug>/",api_views.CourseDetailAPI.as_view()),
    path("detail/<slug:epi_slug>/",api_views.EpisodeDetailAPI.as_view())
]   