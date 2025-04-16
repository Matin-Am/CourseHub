from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Course
from django.contrib import messages
from .cart import Cart



# Create your views here.

class CartDetailView(LoginRequiredMixin ,View):
    def get(self,request):  
        cart = Cart(request , request.user.username)
        return render(request,"order/cart.html", {"cart": cart})

class CartAddView(LoginRequiredMixin,View):
    def get(self,request,course_slug):
        cart = Cart(request , request.user.username , course_slug)
        if request.session['course_data'][request.user.username][course_slug] != {}:
            messages.error(request,"You already have this course in your cart","danger")
        else:
            cart.add(request)
            messages.success(request,"Your course has been added to cart successfully","success")
            print(request.session["course_data"])
        return redirect("home:home")
            
class CartRemoveView(LoginRequiredMixin , View):
    def get(self,request , course_slug):
        if request.session['course_data'][request.user.username][course_slug]:
            cart = Cart(request,request.user.username , course_slug)
            cart.remove()
            messages.success(request,"Course has been removed from cart",'success')
        else:
            messages.error(request,"You already dont have this course in your cart",'danger')
        return redirect("order:cart")