from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm
from django.contrib.auth import authenticate , login , logout
from .models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import pytz
from utils import Data
# Create your views here.


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)


    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            data = Data(request,cd["username"],str(datetime.now(tz=pytz.timezone("Asia/Tehran"))))
            data.save_data(cd["email"])
            messages.success(request,"User has been registered successfully","success")
            return redirect("home:home")
        return render(request,self.template_name,{"form":form})
    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name ,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
            if user is not None:
                login(request,user) 
                messages.success(request,"User has been logged in successfully",'success')
                data = Data(request,form.cleaned_data["username"],str(datetime.now(tz=pytz.timezone("Asia/Tehran"))))
                data.save_last_login(request)
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            else:
                messages.error(request,"Username or password is wrong","danger")
                return redirect("accounts:login")
        return render(request,self.template_name ,{'form':form})
    

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"User logged out successfully","success")
        return redirect("home:home")    
