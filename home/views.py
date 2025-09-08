from django.shortcuts import render ,redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from .models import Episode , Course
from .forms import SearchForm
# Create your views here.


class HomeView(View):
    form_class = SearchForm
    def get(self,request):
        search = request.GET.get("search")
        courses = cache.get_or_set(f"courses_list_{request.user.id}",
                                   lambda:Course.objects.all(),timeout= 60 * 15 )
        if search:
            courses = courses.filter(title__icontains=search)
        return render(request,"home/home.html",{"courses":courses,"form":self.form_class})


class VideoDetailView(LoginRequiredMixin,View):    
    def get(self,request , epi_slug):
        episode = get_object_or_404(Episode , slug=epi_slug)
        if episode.course.paid is False:
            messages.error(request,"You cant watch this video", 'danger')
            return redirect("home:home")
        return render(request,"home/detail.html",{"episode":episode})


