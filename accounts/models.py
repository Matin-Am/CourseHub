from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime , timedelta
from django.utils import timezone
# Create your models here.



class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(max_length=100,  unique=True)
    email = models.EmailField(max_length=100 , unique=True )
    date_joined  = models.DateTimeField(auto_now_add=True)
    is_staff =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
    
    def __str__(self):
        return f"{self.username} - {self.email}"


class OtpCode(models.Model):
    code = models.SmallIntegerField()
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return self.created < timezone.now() - timedelta(minutes=3)

    def __str__(self):
        return f"{self.email} - {self.code}"