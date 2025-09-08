from django.shortcuts import render ,redirect, get_object_or_404
from django.views import View
from .models import Episode , Course
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
# Create your views here.


class HomeView(View):
    def get(self,request):
        courses = cache.get_or_set(f"courses_list_{request.user.id}",
                                   lambda:list(Course.objects.all()),timeout= 60 * 15 )
        return render(request,"home/home.html",{"courses":courses})


class VideoDetailView(LoginRequiredMixin,View):    
    def get(self,request , epi_slug):
        episode = get_object_or_404(Episode , slug=epi_slug)
        if episode.course.paid is False:
            messages.error(request,"You cant watch this video", 'danger')
            return redirect("home:home")
        return render(request,"home/detail.html",{"episode":episode})


