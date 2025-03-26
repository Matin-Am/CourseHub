from django import forms
from accounts.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username","email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd['password2'] and cd["password1"] != cd['password2']:
            raise ValidationError("Passwords must match !!!")
        return cd['password2']

    def save(self , commit=True):
        user =  super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password from <a href=\'../password/\'>this link <a/>")
    class Meta:
        model = User
        fields = ("username","email","password", "is_active", "is_staff")
        


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("This user with this username already regsitered ! ")
        return username
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This user with this email already regsitered ! ")
        return email
    
    def clean(self):
        cd =  super().clean()
        p1 = cd["password"]
        p2 = cd["password2"]
        if p1 and p2 and p1 != p2 :
            raise ValidationError("Passwords must match ! ")
        return cd

class UserReigisterVerifyCodeForm(forms.Form):
    code = forms.IntegerField()




class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter username","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"enter password","class":"form-control"}))
