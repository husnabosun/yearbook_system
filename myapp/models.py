import pandas as pd
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create__user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', null=True)
    username = models.CharField(max_length=200, unique=True, blank=True, default='')
    student_number = models.IntegerField(blank=True, default=0)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or str(self.email).split('@')[0]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    username = models.TextField(max_length=128)
    student_number = models.IntegerField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class ApproveNote(models.Model):
    STATUS_CHOICES = {
        'pending': 'pending',
        'approved': 'approved',
        'disapproved': 'disapproved',
    }
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')


class Note(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE, default=None)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE,default=None)
    text = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('disapproved', 'disapproved'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Note from {self.sender} to {self.recipient} at {self.timestamp}"




