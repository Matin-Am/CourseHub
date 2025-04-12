from django.shortcuts import render ,redirect, get_object_or_404
from django.views import View
from .models import Episode , Course
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
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

class CartAddView(LoginRequiredMixin,View):
    def get(self,request,course_slug):
        course = get_object_or_404(Course , slug=course_slug)
        cart = Cart(request , request.user.username , course)
        if request.session['course_data'][request.user.username][str(course)] != {}:
            messages.error(request,"You already have this course in your cart","danger")

        else:
            cart.add(request)
            messages.success(request,"Your course has been added to cart successfully","success")
            print(request.session["course_data"])
        return redirect("home:home")
            
