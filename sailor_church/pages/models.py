from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('Email Adress', unique=True)
    surname = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True, region=None)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname']

    def __str__(self):
        return f"{self.first_name} {self.surname}: {self.email}"
    
class ConnectGroup(models.Model): 
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through = 'Membership',
        related_name = 'joined_groups',
    )

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    connect_group = models.ForeignKey(ConnectGroup, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)