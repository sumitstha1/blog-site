from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from base.email import send_email_token_otp_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
import random

# Create your models here.

class Genders(BaseModel):
    gender_name = models.CharField(max_length=10)

class Author(BaseModel):
    profile_picture = models.ImageField(upload_to='author_picture')
    user = models.OneToOneField(User, related_name='author_profile', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=50)
    url = models.URLField(null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.first_name


class Client(BaseModel):
    user = models.OneToOneField(User, related_name='client_profile', on_delete=models.CASCADE)
    gender = models.ForeignKey(Genders, related_name='gender', on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=False)
    is_verified = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.first_name