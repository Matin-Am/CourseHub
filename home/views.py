from django.shortcuts import render ,redirect, get_object_or_404
from django.views import View
from .models import Episode , Course
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomeView(View):
    def get(self,request,course_slug=None):
        episodes = Episode.objects.all()
        courses = Course.objects.all()
        if course_slug:
            course = get_object_or_404(Course , slug=course_slug)
            episodes = course.episodes.all()
        return render(request,"home/home.html",{"episodes":episodes,"courses":courses})
    

class VideoDetailView(View):
    def get(self,request , vid_slug):
        episode = get_object_or_404(Episode , slug=vid_slug)
        if episode.course.paid == False:
            messages.error(request,"You cant watch this video", 'danger')
            return redirect("home:home")
        return render(request,"home/detail.html",{"episode":episode})


