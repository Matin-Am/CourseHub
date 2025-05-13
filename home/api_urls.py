from . import api_views
from django.urls import path
from rest_framework.routers import SimpleRouter



urlpatterns = [
    path("course/",api_views.CourseListAPI.as_view()),
    path("course/<slug:course_slug>/",api_views.CourseDetailAPI.as_view()),
    path("detail/<slug:epi_slug>/",api_views.EpisodeDetailAPI.as_view()),
    # path("comment/<slug:course_slug>/",api_views.CommentAPI.as_view()),
    # path("comment/<slug:course_slug>/<int:comment_id>/",api_views.CommentAPI.as_view()),
    # path("comment/delete/<int:comment_id>/",api_views.CommentDeleteAPI.as_view()),
    # path("comments/<slug:course_slug>/",api_views.CommentListAPI.as_view()),

]   

router = SimpleRouter()
router.register("comment",api_views.CommentViewSet,basename='comment')
urlpatterns += router.urls