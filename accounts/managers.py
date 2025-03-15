from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self,username,email,date_joined,password):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have email")

        user =  self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,date_joined,password):
        user = self.create_user(username,email,date_joined,password)
        user.is_admin = True
        user.save(using=self._db)
        return user