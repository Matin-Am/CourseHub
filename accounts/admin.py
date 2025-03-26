from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm , UserChangeForm
from .models import User , OtpCode
from django.contrib.auth.models import Group

from django.contrib.sessions.models import Session


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ("username","email","is_staff")
    list_filter = ("is_staff",)
    fieldsets = (
        ("Main",{"fields":("username","email","password","last_login")}),
        ("Permissions",{"fields":("is_active","is_staff","is_superuser", "user_permissions","groups")}),
    )
    add_fieldsets = (
        ("Main",{"fields":("username","email","password1","password2","is_superuser")}),
    )
    
    search_fields = ("username","email")
    ordering = ("-date_joined",)    
    filter_horizontal = ("user_permissions","groups")
    
    def get_form(self, request, obj =None, **kwargs):
        form =  super().get_form(request, obj, **kwargs)
        if  not request.user.is_superuser:
            form.base_fields["is_superuser"].disabled = True
        return form


admin.site.register(User,UserAdmin)
admin.site.register(Session)
admin.site.register(OtpCode)