from django.shortcuts import render
from django.views import View
from .models import Episode , Course
# Create your views here.


class HomeView(View):
    def get(self,request,course_slug=None):
        episodes = Episode.objects.all()
        courses = Course.objects.all()
        if course_slug:
            course = Course.objects.get(slug=course_slug)
            episodes = episodes.filter(course=course)
        return render(request,"home/home.html",{"episodes":episodes,"courses":courses})
    

class VideoDetailView(View):
    def get(self,request , vid_slug):
        episode = Episode.objects.get(slug=vid_slug)
        return render(request,"home/detail.html",{"episode":episode})