from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm , UserReigisterVerifyCodeForm
from django.contrib.auth import authenticate , login , logout
from .models import User , OtpCode
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import pytz
from utils import Data , send_otp_code , generate_random_password
import random

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
            random_code = random.randint(100000,999999)
            OtpCode.objects.create(code=random_code,email=cd['email'])
            send_otp_code(random_code,cd['email'])
            data = Data(request,cd["username"],str(datetime.now(tz=pytz.timezone("Asia/Tehran"))))
            data.save_data(cd["email"])
            return redirect("accounts:verify_code")
        return render(request,self.template_name,{"form":form})

class UserVerifyRegisterCodeView(View):
    form_class = UserReigisterVerifyCodeForm
    template_name = "accounts/verify_code.html"
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,context={"form":form})
    def post(self,request):
        form = self.form_class(request.POST)
        print("Session Data:", request.session.get("user_data", {}))  
        session = request.session["user_data"]
        username_session = list(session.keys())[0]
        code_instance = OtpCode.objects.get(email=session[username_session]["email"])
        if form.is_valid():
            if code_instance.code == form.cleaned_data["code"]:
                user = User.objects.create_user(username=username_session,email=session[username_session]["email"],password=generate_random_password())
                user.set_unusable_password()
                user.save()
                messages.success(request,"User has been created successfully","success")
                code_instance.delete()
                return redirect("home:home")
            else:
                messages.error(request,"code is wrong please try again !","danger")
                return redirect("accounts:verify_code")
        return render(request,self.template_name,context={"form":form})

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
