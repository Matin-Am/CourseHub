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
        fields = ("username","email","password", "is_active", "is_admin")
        
