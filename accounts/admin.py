from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm , UserChangeForm
from .models import User
from django.contrib.auth.models import Group
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("username","email","is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("Main",{"fields":("username","email","password","last_login")}),
        ("Permissions",{"fields":("is_active","is_admin")}),
    )
    add_fieldsets = (
        ("Main",{"fields":("username","email","password1","password2",)}),
    )
    
    search_fields = ("username","email")
    ordering = ("-date_joined",)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)