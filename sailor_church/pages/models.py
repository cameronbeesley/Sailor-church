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
    date_joined = models.DateField(auto_now_add=True)

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

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    connect_group = models.ForeignKey(ConnectGroup, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

class JoinRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    connect_group = models.ForeignKey(
        ConnectGroup, 
        on_delete=models.CASCADE,
        related_name='join_requests'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='join_requests'
    )

    status=models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['connect_group', 'user'],
                condition=models.Q(status='pending'),
                name='unique_pending_request_per_user_group'
            )
        ]
    
    def __str__(self):
        return f"{self.user} → {self.connect_group} ({self.status})"



