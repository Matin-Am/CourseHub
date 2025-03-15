from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.



class User(AbstractBaseUser):
    username = models.CharField(max_length=100,  unique=True)
    email = models.EmailField(max_length=100 , unique=True )
    date_joined  = models.DateTimeField(auto_now_add=True)
    is_admin =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
    
    def __str__(self):
        return f"{self.username} - {self.email}"
    
    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin