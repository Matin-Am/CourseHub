from django.shortcuts import render ,redirect, get_object_or_404
from django.views import View
from .models import Episode , Course
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.


class HomeView(View):
    @method_decorator(cache_page(60 * 30,key_prefix="courses"))
    def get(self,request,course_slug=None):
        episodes = None
        courses = Course.objects.all()
        if course_slug:
            course = get_object_or_404(Course , slug=course_slug)
            episodes = course.episodes.all()
        return render(request,"home/home.html",{"episodes":episodes,"courses":courses})
    

class VideoDetailView(View):
    @method_decorator(cache_page(60 * 30,key_prefix="episode"))
    def get(self,request , epi_slug):
        episode = get_object_or_404(Episode , slug=epi_slug)
        if episode.course.paid is False:
            messages.error(request,"You cant watch this video", 'danger')
            return redirect("home:home")
        return render(request,"home/detail.html",{"episode":episode})


