from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self,first_name, username, email,level, roll_number, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            first_name = first_name,
            email = self.normalize_email(email),
            username = username,
            password = password,
            level = level,
            roll_number = roll_number,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,username, email, password):
        user = self.create_user(
            first_name = first_name,
            email = self.normalize_email(email),
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        
        user.save(using=self._db)
        return user
    

#Account here referst to the students 
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    roll_number = models.CharField(max_length=5, blank=True)
    level = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username']

    def __str__(self):
        return self.first_name
    

    objects = MyAccountManager()

     #this is for superadmin and admin roles
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True