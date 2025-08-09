from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WORKER = 'worker', 'Worker'
        
    username = None
    email = models.EmailField(unique=True, blank= False, null= False, max_length=100)
    role = models.CharField(max_length=10, choices=UserType.choices)
        
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    
    
    def __str__(self):
        return f'The account {self.email} is a {self.role}'
        
    